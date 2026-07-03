"""
Payment notification API views for Ledger integration.

These views handle background payment notifications from the Ledger payment system.
They are session-less and designed to be called by external systems, not end users.
"""

import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from mooring.models import Booking, AdmissionsBooking

logger = logging.getLogger(__name__)


class BookingPaymentNotificationView(APIView):
    """
    Revised endpoint to handle Ledger payment notifications.
    Supports both GET (observed in logs) and POST (original spec).
    """
    
    # No authentication required for this callback
    authentication_classes = []
    permission_classes = []
    
    def get(self, request, pk, format=None):
        # Extract invoice from query string (?invoice=XXXX)
        logger.info(f"Received GET payment notification for booking {pk} with query params: {request.query_params}")

        invoice_ref = request.query_params.get('invoice') or request.query_params.get('invoice_reference')
        return self._handle_notification(request, pk, invoice_ref)

    def post(self, request, pk, format=None):
        # Extract invoice from POST body or query string
        logger.info(f"Received POST payment notification for booking {pk} with body: {request.data}")

        invoice_ref = request.data.get('invoice') or request.data.get('invoice_reference') or request.query_params.get('invoice')
        return self._handle_notification(request, pk, invoice_ref)

    def _handle_notification(self, request, pk, invoice_reference):
        # Client IP for logging
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        client_ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR', 'unknown')
        
        logger.info(f"Payment notification received for booking {pk}, invoice {invoice_reference} from IP {client_ip}")

        if not invoice_reference:
            logger.error(f"Missing invoice reference for booking {pk}")
            return Response({'error': 'Missing invoice_reference'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Note: booking.id might be int or uuid depending on your model
            booking = Booking.objects.get(id=pk)
            
            # CRITICAL: Ensure this method is fixed to handle update_payments() correctly
            context = booking.process_payment_notification(invoice_reference)
            
            # Send emails (ensure this handles context safely)
            booking.send_payment_emails(context)
            
            return Response({
                'status': 'success',
                'booking_id': str(pk),
                'invoice': invoice_reference
            }, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            logger.error(f"Booking {pk} not found during payment notification")
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Capture full stack trace for debugging the update_payments error
            logger.error(f"Error processing notification for booking {pk}: {str(e)}", exc_info=True)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdmissionsPaymentNotificationView(APIView):
    """
    Revised endpoint for Ledger to notify about admissions booking payment completion.
    Supports both GET (Ledger default) and POST.
    """
    
    authentication_classes = []
    permission_classes = []
    
    def get(self, request, pk, format=None):
        """
        Handle GET requests from Ledger.
        """
        # Extract invoice from query string (?invoice=XXXX)
        invoice_reference = request.query_params.get('invoice') or request.query_params.get('invoice_reference')
        return self._handle_notification(request, pk, invoice_reference)

    def post(self, request, pk, format=None):
        """
        Handle POST requests for backward compatibility.
        """
        # Extract from POST data or fallback to query params
        invoice_reference = (request.data.get('invoice') or 
                           request.data.get('invoice_reference') or 
                           request.query_params.get('invoice'))
        return self._handle_notification(request, pk, invoice_reference)

    def _handle_notification(self, request, pk, invoice_reference):
        """
        Shared logic for processing admissions payment notifications.
        """
        # Get client IP for audit logging
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        client_ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR', 'unknown')
        
        logger.info(f'Admissions payment notification received: booking_id={pk}, '
                   f'invoice={invoice_reference}, ip={client_ip}')
        
        if not invoice_reference:
            logger.warning(f'Admissions payment notification rejected: missing invoice, '
                          f'booking_id={pk}, ip={client_ip}')
            return Response({'error': 'Missing invoice'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Note: Ensure pk matches your model ID type (int or uuid)
            booking = AdmissionsBooking.objects.get(id=pk)
            
            # Process payment notification (idempotent)
            context = booking.process_payment_notification(invoice_reference)
            
            # Send confirmation emails
            booking.send_payment_emails(context)
            
            logger.info(f'Admissions notification processed successfully: '
                       f'booking_id={pk}, invoice={invoice_reference}, ip={client_ip}')
            
            return Response({
                'status': 'success',
                'booking_id': str(pk),
                'invoice': invoice_reference
            }, status=status.HTTP_200_OK)
            
        except AdmissionsBooking.DoesNotExist:
            logger.error(f'Admissions booking not found: {pk}')
            return Response({'error': 'Admissions booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error processing admissions notification: {str(e)}', exc_info=True)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)