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
    Session-less endpoint for Ledger to notify about payment completion.
    Booking is identified by UUID (booking_token URL parameter) only; the invoice
    is looked up from the submitted Ledger basket, not taken from the request.
    Supports both GET (observed in logs) and POST (original spec).
    """

    # No authentication required for this callback
    authentication_classes = []
    permission_classes = []

    def get(self, request, booking_token, format=None):
        logger.info(f"Received GET payment notification for booking {booking_token}")
        return self._handle_notification(request, booking_token)

    def post(self, request, booking_token, format=None):
        logger.info(f"Received POST payment notification for booking {booking_token}")
        return self._handle_notification(request, booking_token)

    def _handle_notification(self, request, booking_token):
        # Client IP for logging
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        client_ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR', 'unknown')

        logger.info(f"Payment notification received for booking {booking_token} from IP {client_ip}")

        try:
            booking = Booking.objects.get(uuid=booking_token)

            was_already_processed = (booking.booking_type == 1)
            context = booking.process_payment_notification()
            # process_payment_notification() is idempotent but send_payment_emails() is not.
            if not was_already_processed:
                booking.send_payment_emails(context)

            return Response({
                'status': 'success',
                'booking_id': str(booking_token),
            }, status=status.HTTP_200_OK)

        except Booking.DoesNotExist:
            logger.error(f"Booking {booking_token} not found during payment notification")
            return Response({'error': 'Booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f"Error processing notification for booking {booking_token}: {str(e)}", exc_info=True)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdmissionsPaymentNotificationView(APIView):
    """
    Session-less endpoint for Ledger to notify about admissions booking payment completion.
    AdmissionsBooking is identified by UUID (booking_token URL parameter) only; the invoice
    is looked up from the submitted Ledger basket, not taken from the request.
    Supports both GET (Ledger default) and POST.
    """

    authentication_classes = []
    permission_classes = []

    def get(self, request, booking_token, format=None):
        logger.info(f"Received GET admissions payment notification for booking {booking_token}")
        return self._handle_notification(request, booking_token)

    def post(self, request, booking_token, format=None):
        logger.info(f"Received POST admissions payment notification for booking {booking_token}")
        return self._handle_notification(request, booking_token)

    def _handle_notification(self, request, booking_token):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        client_ip = x_forwarded_for.split(',')[0].strip() if x_forwarded_for else request.META.get('REMOTE_ADDR', 'unknown')

        logger.info(f'Admissions payment notification received: booking_token={booking_token}, ip={client_ip}')

        try:
            booking = AdmissionsBooking.objects.get(uuid=booking_token)

            was_already_processed = (booking.booking_type == 1)
            context = booking.process_payment_notification()
            # process_payment_notification() is idempotent but send_payment_emails() is not.
            if not was_already_processed:
                booking.send_payment_emails(context)

            logger.info(f'Admissions notification processed successfully: '
                        f'booking_token={booking_token}, ip={client_ip}')

            return Response({
                'status': 'success',
                'booking_token': str(booking_token),
            }, status=status.HTTP_200_OK)

        except AdmissionsBooking.DoesNotExist:
            logger.error(f'Admissions booking not found for uuid: {booking_token}')
            return Response({'error': 'Admissions booking not found'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            logger.error(f'Error processing admissions notification for {booking_token}: {str(e)}', exc_info=True)
            return Response({'error': 'Internal server error'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)