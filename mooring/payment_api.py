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
    Session-less endpoint for Ledger to notify about booking payment completion.
    
    This endpoint is called by the Ledger payment system when a payment is completed.
    It processes the payment (idempotently) and sends confirmation emails.
    
    HTTP Method: POST only
    URL Pattern: /api/booking-payment-notification/<uuid:pk>/
    Authentication: None (invoice ownership validated via basket.booking_reference)
    
    Request Body:
        {
            "invoice_reference": "INV-123456"
        }
    
    Response (Success - 200):
        {
            "status": "success",
            "booking_id": "uuid-string",
            "invoice": "INV-123456"
        }
    
    Response (Error):
        - 400: Missing or invalid invoice_reference
        - 404: Booking not found
        - 500: Internal server error
    """
    
    # Disable authentication - this is called by external systems
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, pk, format=None):
        """
        Process payment notification for a booking.
        
        Args:
            request: Django REST framework request object
            pk: UUID of the booking
            format: Optional format suffix (not used)
        
        Returns:
            Response: JSON response with success/error status
        """
        # Get client IP for audit logging
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0].strip()
        else:
            client_ip = request.META.get('REMOTE_ADDR', 'unknown')
        
        # Parse input
        invoice_reference = request.data.get('invoice_reference')
        
        # Log all incoming requests for audit trail
        logger.info(f'Payment notification received: booking_id={pk}, '
                   f'invoice={invoice_reference}, ip={client_ip}')
        
        # Validate input
        if not invoice_reference:
            logger.warning(f'Payment notification rejected: missing invoice_reference, '
                          f'booking_id={pk}, ip={client_ip}')
            return Response(
                {'error': 'Missing invoice_reference'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate invoice reference format (should start with appropriate prefix)
        if not invoice_reference.strip():
            logger.warning(f'Payment notification rejected: empty invoice_reference, '
                          f'booking_id={pk}, ip={client_ip}')
            return Response(
                {'error': 'Invalid invoice_reference format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get booking
            booking = Booking.objects.get(id=pk)
            
            # Process payment notification (idempotent, atomic transaction)
            context = booking.process_payment_notification(invoice_reference)
            
            # Send confirmation emails (errors logged but don't fail)
            booking.send_payment_emails(context)
            
            # Log success
            logger.info(f'Payment notification processed successfully: '
                       f'booking_id={pk}, invoice={invoice_reference}, '
                       f'customer={booking.customer.get_full_name() if booking.customer else "Anonymous"}, '
                       f'ip={client_ip}')
            
            return Response({
                'status': 'success',
                'booking_id': str(pk),
                'invoice': invoice_reference
            }, status=status.HTTP_200_OK)
            
        except Booking.DoesNotExist:
            logger.error(f'Payment notification failed: booking not found, '
                        f'booking_id={pk}, invoice={invoice_reference}, ip={client_ip}')
            return Response(
                {'error': 'Booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        except ValueError as e:
            # Invoice validation errors (wrong system, wrong basket, etc.)
            logger.error(f'Payment notification failed: validation error, '
                        f'booking_id={pk}, invoice={invoice_reference}, '
                        f'error={str(e)}, ip={client_ip}')
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            # Unexpected errors
            logger.error(f'Payment notification failed: unexpected error, '
                        f'booking_id={pk}, invoice={invoice_reference}, '
                        f'error={str(e)}, ip={client_ip}',
                        exc_info=True)
            return Response(
                {'error': 'Internal server error processing payment notification'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AdmissionsPaymentNotificationView(APIView):
    """
    Session-less endpoint for Ledger to notify about admissions booking payment completion.
    
    This endpoint is called by the Ledger payment system when a payment is completed.
    It processes the payment (idempotently) and sends confirmation emails.
    
    HTTP Method: POST only
    URL Pattern: /api/admissions-payment-notification/<uuid:pk>/
    Authentication: None (invoice ownership validated via basket.booking_reference)
    
    Request Body:
        {
            "invoice_reference": "INV-123456"
        }
    
    Response (Success - 200):
        {
            "status": "success",
            "booking_id": "uuid-string",
            "invoice": "INV-123456"
        }
    
    Response (Error):
        - 400: Missing or invalid invoice_reference
        - 404: Admissions booking not found
        - 500: Internal server error
    """
    
    # Disable authentication - this is called by external systems
    authentication_classes = []
    permission_classes = []
    
    def post(self, request, pk, format=None):
        """
        Process payment notification for an admissions booking.
        
        Args:
            request: Django REST framework request object
            pk: UUID of the admissions booking
            format: Optional format suffix (not used)
        
        Returns:
            Response: JSON response with success/error status
        """
        # Get client IP for audit logging
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            client_ip = x_forwarded_for.split(',')[0].strip()
        else:
            client_ip = request.META.get('REMOTE_ADDR', 'unknown')
        
        # Parse input
        invoice_reference = request.data.get('invoice_reference')
        
        # Log all incoming requests for audit trail
        logger.info(f'Admissions payment notification received: booking_id={pk}, '
                   f'invoice={invoice_reference}, ip={client_ip}')
        
        # Validate input
        if not invoice_reference:
            logger.warning(f'Admissions payment notification rejected: missing invoice_reference, '
                          f'booking_id={pk}, ip={client_ip}')
            return Response(
                {'error': 'Missing invoice_reference'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Validate invoice reference format (should start with appropriate prefix)
        if not invoice_reference.strip():
            logger.warning(f'Admissions payment notification rejected: empty invoice_reference, '
                          f'booking_id={pk}, ip={client_ip}')
            return Response(
                {'error': 'Invalid invoice_reference format'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Get admissions booking
            booking = AdmissionsBooking.objects.get(id=pk)
            
            # Process payment notification (idempotent, atomic transaction)
            context = booking.process_payment_notification(invoice_reference)
            
            # Send confirmation emails (errors logged but don't fail)
            booking.send_payment_emails(context)
            
            # Log success
            logger.info(f'Admissions payment notification processed successfully: '
                       f'booking_id={pk}, invoice={invoice_reference}, '
                       f'customer={booking.customer.get_full_name() if booking.customer else "Anonymous"}, '
                       f'ip={client_ip}')
            
            return Response({
                'status': 'success',
                'booking_id': str(pk),
                'invoice': invoice_reference
            }, status=status.HTTP_200_OK)
            
        except AdmissionsBooking.DoesNotExist:
            logger.error(f'Admissions payment notification failed: booking not found, '
                        f'booking_id={pk}, invoice={invoice_reference}, ip={client_ip}')
            return Response(
                {'error': 'Admissions booking not found'},
                status=status.HTTP_404_NOT_FOUND
            )
            
        except ValueError as e:
            # Invoice validation errors (wrong system, wrong basket, etc.)
            logger.error(f'Admissions payment notification failed: validation error, '
                        f'booking_id={pk}, invoice={invoice_reference}, '
                        f'error={str(e)}, ip={client_ip}')
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        except Exception as e:
            # Unexpected errors
            logger.error(f'Admissions payment notification failed: unexpected error, '
                        f'booking_id={pk}, invoice={invoice_reference}, '
                        f'error={str(e)}, ip={client_ip}',
                        exc_info=True)
            return Response(
                {'error': 'Internal server error processing payment notification'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
