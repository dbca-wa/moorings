"""
Test suite for payment notification API endpoints.

Tests the BookingPaymentNotificationView and AdmissionsPaymentNotificationView
endpoints that handle background payment notifications from Ledger.
"""
from .test_setup import TestSetup
from django.test import Client, RequestFactory
from django.urls import reverse
from mixer.backend.django import mixer
from datetime import datetime, timedelta
from decimal import Decimal
from unittest.mock import patch, MagicMock, Mock
import json

from .models import (
    Booking, 
    AdmissionsBooking, 
    BookingInvoice, 
    AdmissionsBookingInvoice,
    MooringArea,
    Mooringsite,
    MooringsiteBooking
)
from ledger_api_client.ledger_models import Invoice, Basket
from ledger_api_client.order import Order


class BookingPaymentNotificationTestCase(TestSetup):
    """Test suite for Booking payment notification endpoint."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        
        # Create test mooring area and site
        self.mooring_area = mixer.blend(
            MooringArea,
            name='Test Marina',
            mooring_type=0
        )
        self.mooring_site = mixer.blend(
            Mooringsite,
            mooringarea=self.mooring_area
        )
        
        # Create test booking (temporary - booking_type=3)
        self.booking = mixer.blend(
            Booking,
            booking_type=3,  # temporary
            customer=self.testAdmin,
            cost_total=Decimal('100.00'),
            override_price=Decimal('100.00'),
            mooringarea=self.mooring_area,
            arrival=(datetime.now() + timedelta(days=7)).date(),
            departure=(datetime.now() + timedelta(days=10)).date(),
            details={'vessel_rego': 'TEST123', 'vessel_size': '10.5', 'vessel_draft': '2.0', 'vessel_beam': '3.5', 'vessel_weight': '5000'}
        )
        
        # Create mooring site booking
        self.site_booking = mixer.blend(
            MooringsiteBooking,
            booking=self.booking,
            campsite=self.mooring_site,
            from_dt=datetime.now() + timedelta(days=7),
            to_dt=datetime.now() + timedelta(days=10),
            amount=Decimal('100.00')
        )
        
        self.url = reverse('api-booking-payment-notification', kwargs={'pk': self.booking.id})
        self.invoice_ref = 'INV-TEST-001'
    
    def _mock_invoice_and_basket(self, invoice_ref, booking_ref_prefix, system='0516'):
        """Helper to mock Invoice and Basket objects."""
        mock_invoice = MagicMock(spec=Invoice)
        mock_invoice.reference = invoice_ref
        mock_invoice.system = system
        mock_invoice.order_number = 'ORD-001'
        mock_invoice.owner = self.testAdmin.id
        
        mock_basket = MagicMock(spec=Basket)
        mock_basket.booking_reference = f'{booking_ref_prefix}{self.booking.id}'
        mock_basket.system = system
        
        return mock_invoice, mock_basket
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    @patch('mooring.models.update_payments')
    def test_successful_notification(self, mock_update_payments, mock_basket_filter, mock_invoice_get):
        """Test successful payment notification processing."""
        # Mock ledger API calls
        mock_invoice, mock_basket = self._mock_invoice_and_basket(self.invoice_ref, 'PS-')
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        mock_update_payments.return_value = None
        
        # Send notification
        response = self.client.post(
            self.url, 
            {'invoice_reference': self.invoice_ref},
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['invoice'], self.invoice_ref)
        
        # Verify booking updated
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.booking_type, 1)  # confirmed
        self.assertIsNone(self.booking.expiry_time)
        
        # Verify BookingInvoice created
        self.assertTrue(
            BookingInvoice.objects.filter(
                booking=self.booking, 
                invoice_reference=self.invoice_ref
            ).exists()
        )
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    @patch('mooring.models.update_payments')
    def test_idempotency(self, mock_update_payments, mock_basket_filter, mock_invoice_get):
        """Test calling notification twice produces same result."""
        # Mock ledger API calls
        mock_invoice, mock_basket = self._mock_invoice_and_basket(self.invoice_ref, 'PS-')
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        mock_update_payments.return_value = None
        
        # First call
        response1 = self.client.post(
            self.url,
            {'invoice_reference': self.invoice_ref},
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 200)
        
        # Second call (should succeed without errors)
        response2 = self.client.post(
            self.url,
            {'invoice_reference': self.invoice_ref},
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, 200)
        
        # Verify no duplicate BookingInvoice records
        invoice_count = BookingInvoice.objects.filter(
            booking=self.booking,
            invoice_reference=self.invoice_ref
        ).count()
        self.assertEqual(invoice_count, 1)
        
        # Verify booking still in correct state
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.booking_type, 1)
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    def test_invoice_ownership_validation(self, mock_basket_filter, mock_invoice_get):
        """Test invoice must belong to the booking."""
        # Mock invoice but no matching basket (ownership validation fails)
        mock_invoice, _ = self._mock_invoice_and_basket(self.invoice_ref, 'PS-')
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = []  # No basket found
        
        response = self.client.post(
            self.url,
            {'invoice_reference': self.invoice_ref},
            content_type='application/json'
        )
        
        # Should return error
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    @patch('mooring.models.Invoice.objects.get')
    def test_nonexistent_invoice(self, mock_invoice_get):
        """Test validation rejects non-existent invoices."""
        mock_invoice_get.side_effect = Invoice.DoesNotExist('Invoice not found')
        
        response = self.client.post(
            self.url,
            {'invoice_reference': 'INV-FAKE'},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_invalid_booking_id(self):
        """Test 404 for non-existent booking."""
        url = reverse('api-booking-payment-notification', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})
        response = self.client.post(
            url,
            {'invoice_reference': self.invoice_ref},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    def test_wrong_system_invoice(self, mock_basket_filter, mock_invoice_get):
        """Test validation rejects wrong system invoices."""
        # Mock invoice with wrong system
        mock_invoice, mock_basket = self._mock_invoice_and_basket(self.invoice_ref, 'PS-', system='9999')
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        
        response = self.client.post(
            self.url,
            {'invoice_reference': self.invoice_ref},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_missing_invoice_reference(self):
        """Test validation rejects missing invoice_reference."""
        response = self.client.post(
            self.url,
            {},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)


class AdmissionsPaymentNotificationTestCase(TestSetup):
    """Test suite for AdmissionsBooking payment notification endpoint."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        
        # Create test mooring area
        self.mooring_area = mixer.blend(
            MooringArea,
            name='Test Marina',
            mooring_type=0
        )
        
        # Create test admissions booking (temporary - booking_type=3)
        self.booking = mixer.blend(
            AdmissionsBooking,
            booking_type=3,  # temporary
            customer=self.testAdmin,
            cost_total=Decimal('50.00'),
            override_price=Decimal('50.00'),
            location=self.mooring_area
        )
        
        self.url = reverse('api-admissions-payment-notification', kwargs={'pk': self.booking.id})
        self.invoice_ref = 'INV-TEST-AD-001'
    
    def _mock_invoice_and_basket(self, invoice_ref, booking_ref_prefix, system='0516'):
        """Helper to mock Invoice and Basket objects."""
        mock_invoice = MagicMock(spec=Invoice)
        mock_invoice.reference = invoice_ref
        mock_invoice.system = system
        mock_invoice.order_number = 'ORD-AD-001'
        mock_invoice.owner = self.testAdmin.id
        
        mock_basket = MagicMock(spec=Basket)
        mock_basket.booking_reference = f'{booking_ref_prefix}{self.booking.id}'
        mock_basket.system = system
        
        return mock_invoice, mock_basket
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    @patch('mooring.models.update_payments')
    def test_successful_notification(self, mock_update_payments, mock_basket_filter, mock_invoice_get):
        """Test successful admissions payment notification processing."""
        # Mock ledger API calls
        mock_invoice, mock_basket = self._mock_invoice_and_basket(self.invoice_ref, 'AD-')
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        mock_update_payments.return_value = None
        
        # Send notification
        response = self.client.post(
            self.url,
            {'invoice_reference': self.invoice_ref},
            content_type='application/json'
        )
        
        # Verify response
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['status'], 'success')
        self.assertEqual(data['invoice'], self.invoice_ref)
        
        # Verify booking updated
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.booking_type, 1)  # confirmed
        
        # Verify AdmissionsBookingInvoice created
        self.assertTrue(
            AdmissionsBookingInvoice.objects.filter(
                admissions_booking=self.booking,
                invoice_reference=self.invoice_ref
            ).exists()
        )
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    @patch('mooring.models.update_payments')
    def test_idempotency(self, mock_update_payments, mock_basket_filter, mock_invoice_get):
        """Test calling notification twice produces same result."""
        # Mock ledger API calls
        mock_invoice, mock_basket = self._mock_invoice_and_basket(self.invoice_ref, 'AD-')
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        mock_update_payments.return_value = None
        
        # First call
        response1 = self.client.post(
            self.url,
            {'invoice_reference': self.invoice_ref},
            content_type='application/json'
        )
        self.assertEqual(response1.status_code, 200)
        
        # Second call
        response2 = self.client.post(
            self.url,
            {'invoice_reference': self.invoice_ref},
            content_type='application/json'
        )
        self.assertEqual(response2.status_code, 200)
        
        # Verify no duplicate records
        invoice_count = AdmissionsBookingInvoice.objects.filter(
            admissions_booking=self.booking,
            invoice_reference=self.invoice_ref
        ).count()
        self.assertEqual(invoice_count, 1)
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    def test_invoice_ownership_validation(self, mock_basket_filter, mock_invoice_get):
        """Test invoice must belong to the admissions booking."""
        # Mock invoice but no matching basket
        mock_invoice, _ = self._mock_invoice_and_basket(self.invoice_ref, 'AD-')
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = []
        
        response = self.client.post(
            self.url,
            {'invoice_reference': self.invoice_ref},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
        data = json.loads(response.content)
        self.assertIn('error', data)
    
    def test_invalid_booking_id(self):
        """Test 404 for non-existent admissions booking."""
        url = reverse('api-admissions-payment-notification', kwargs={'pk': '00000000-0000-0000-0000-000000000000'})
        response = self.client.post(
            url,
            {'invoice_reference': self.invoice_ref},
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 404)


class BookingPaymentProcessingTestCase(TestSetup):
    """Unit tests for Booking.process_payment_notification() model method."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        
        # Create test mooring area and site
        self.mooring_area = mixer.blend(
            MooringArea,
            name='Test Marina',
            mooring_type=0
        )
        self.mooring_site = mixer.blend(
            Mooringsite,
            mooringarea=self.mooring_area
        )
        
        # Create test booking (temporary)
        self.booking = mixer.blend(
            Booking,
            booking_type=3,  # temporary
            customer=self.testAdmin,
            cost_total=Decimal('100.00'),
            override_price=Decimal('100.00'),
            mooringarea=self.mooring_area,
            arrival=(datetime.now() + timedelta(days=7)).date(),
            departure=(datetime.now() + timedelta(days=10)).date(),
            details={'vessel_rego': 'TEST123', 'vessel_size': '10.5', 'vessel_draft': '2.0', 'vessel_beam': '3.5', 'vessel_weight': '5000'},
            expiry_time=datetime.now() + timedelta(hours=2)
        )
        
        # Create mooring site booking
        self.site_booking = mixer.blend(
            MooringsiteBooking,
            booking=self.booking,
            campsite=self.mooring_site,
            from_dt=datetime.now() + timedelta(days=7),
            to_dt=datetime.now() + timedelta(days=10),
            amount=Decimal('100.00')
        )
        
        self.invoice_ref = 'INV-MODEL-TEST-001'
    
    def _mock_ledger_objects(self, invoice_ref, booking_ref_prefix='PS-', system='0516'):
        """Helper to create mock ledger objects."""
        mock_invoice = MagicMock(spec=Invoice)
        mock_invoice.reference = invoice_ref
        mock_invoice.system = system
        mock_invoice.order_number = 'ORD-001'
        
        mock_basket = MagicMock(spec=Basket)
        mock_basket.booking_reference = f'{booking_ref_prefix}{self.booking.id}'
        mock_basket.system = system
        
        return mock_invoice, mock_basket
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    @patch('mooring.models.update_payments')
    def test_process_payment_updates_booking_type(self, mock_update_payments, mock_basket_filter, mock_invoice_get):
        """Test booking_type changes from 3 (temporary) to 1 (confirmed)."""
        # Mock ledger objects
        mock_invoice, mock_basket = self._mock_ledger_objects(self.invoice_ref)
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        mock_update_payments.return_value = None
        
        # Process payment
        context = self.booking.process_payment_notification(self.invoice_ref)
        
        # Verify booking updated
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.booking_type, 1)  # confirmed
        self.assertIsNone(self.booking.expiry_time)
        
        # Verify context returned
        self.assertIn('booking', context)
        self.assertEqual(context['booking'], self.booking)
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    @patch('mooring.models.update_payments')
    def test_process_payment_creates_booking_invoice(self, mock_update_payments, mock_basket_filter, mock_invoice_get):
        """Test BookingInvoice record created."""
        # Mock ledger objects
        mock_invoice, mock_basket = self._mock_ledger_objects(self.invoice_ref)
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        mock_update_payments.return_value = None
        
        # Process payment
        context = self.booking.process_payment_notification(self.invoice_ref)
        
        # Verify BookingInvoice exists
        self.assertTrue(
            BookingInvoice.objects.filter(
                booking=self.booking,
                invoice_reference=self.invoice_ref
            ).exists()
        )
        
        # Verify only one record
        self.assertEqual(
            BookingInvoice.objects.filter(booking=self.booking).count(),
            1
        )
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    @patch('mooring.models.update_payments')
    def test_process_payment_idempotency(self, mock_update_payments, mock_basket_filter, mock_invoice_get):
        """Test calling twice doesn't duplicate state changes."""
        # Mock ledger objects
        mock_invoice, mock_basket = self._mock_ledger_objects(self.invoice_ref)
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        mock_update_payments.return_value = None
        
        # First call
        context1 = self.booking.process_payment_notification(self.invoice_ref)
        
        # Second call
        context2 = self.booking.process_payment_notification(self.invoice_ref)
        
        # Verify same booking in context
        self.assertEqual(context1['booking'].id, context2['booking'].id)
        
        # Verify only one invoice record
        self.assertEqual(
            BookingInvoice.objects.filter(booking=self.booking).count(),
            1
        )
        
        # Verify booking_type still correct
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.booking_type, 1)
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    @patch('mooring.models.update_payments')
    def test_process_payment_handles_old_booking(self, mock_update_payments, mock_basket_filter, mock_invoice_get):
        """Test old_booking cancellation for booking changes."""
        # Create old booking
        old_booking = mixer.blend(
            Booking,
            booking_type=1,  # confirmed
            is_canceled=False,
            customer=self.testAdmin,
            mooringarea=self.mooring_area
        )
        
        # Set old_booking reference
        self.booking.old_booking = old_booking
        self.booking.save()
        
        # Mock ledger objects
        mock_invoice, mock_basket = self._mock_ledger_objects(self.invoice_ref)
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        mock_update_payments.return_value = None
        
        # Process payment for new booking
        context = self.booking.process_payment_notification(self.invoice_ref)
        
        # Verify old booking cancelled
        old_booking.refresh_from_db()
        self.assertTrue(old_booking.is_canceled)
        self.assertEqual(old_booking.booking_type, 4)  # Changed Booking
        self.assertIsNotNone(old_booking.cancelation_time)
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    def test_invoice_validation_wrong_system(self, mock_basket_filter, mock_invoice_get):
        """Test invoice system validation."""
        # Mock invoice with wrong system
        mock_invoice, mock_basket = self._mock_ledger_objects(self.invoice_ref, system='9999')
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.booking.process_payment_notification(self.invoice_ref)
        
        self.assertIn('system', str(context.exception).lower())
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    def test_invoice_validation_ownership(self, mock_basket_filter, mock_invoice_get):
        """Test invoice ownership validation via basket."""
        # Mock invoice but no matching basket (different booking)
        mock_invoice, _ = self._mock_ledger_objects(self.invoice_ref)
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = []  # No basket found
        
        # Should raise ValueError
        with self.assertRaises(ValueError) as context:
            self.booking.process_payment_notification(self.invoice_ref)
        
        self.assertIn('basket', str(context.exception).lower())


class AdmissionsPaymentProcessingTestCase(TestSetup):
    """Unit tests for AdmissionsBooking.process_payment_notification() model method."""
    
    def setUp(self):
        """Set up test fixtures."""
        super().setUp()
        
        # Create test mooring area
        self.mooring_area = mixer.blend(
            MooringArea,
            name='Test Marina',
            mooring_type=0
        )
        
        # Create test admissions booking (temporary)
        self.booking = mixer.blend(
            AdmissionsBooking,
            booking_type=3,  # temporary
            customer=self.testAdmin,
            cost_total=Decimal('50.00'),
            override_price=Decimal('50.00'),
            location=self.mooring_area
        )
        
        self.invoice_ref = 'INV-AD-MODEL-TEST-001'
    
    def _mock_ledger_objects(self, invoice_ref, booking_ref_prefix='AD-', system='0516'):
        """Helper to create mock ledger objects."""
        mock_invoice = MagicMock(spec=Invoice)
        mock_invoice.reference = invoice_ref
        mock_invoice.system = system
        mock_invoice.order_number = 'ORD-AD-001'
        
        mock_basket = MagicMock(spec=Basket)
        mock_basket.booking_reference = f'{booking_ref_prefix}{self.booking.id}'
        mock_basket.system = system
        
        return mock_invoice, mock_basket
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    @patch('mooring.models.update_payments')
    def test_process_payment_updates_booking_type(self, mock_update_payments, mock_basket_filter, mock_invoice_get):
        """Test admissions booking_type changes from 3 to 1."""
        # Mock ledger objects
        mock_invoice, mock_basket = self._mock_ledger_objects(self.invoice_ref)
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        mock_update_payments.return_value = None
        
        # Process payment
        context = self.booking.process_payment_notification(self.invoice_ref)
        
        # Verify booking updated
        self.booking.refresh_from_db()
        self.assertEqual(self.booking.booking_type, 1)  # confirmed
        
        # Verify context returned
        self.assertIn('admissionsBooking', context)
        self.assertEqual(context['admissionsBooking'], self.booking)
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    @patch('mooring.models.update_payments')
    def test_process_payment_creates_admissions_invoice(self, mock_update_payments, mock_basket_filter, mock_invoice_get):
        """Test AdmissionsBookingInvoice record created."""
        # Mock ledger objects
        mock_invoice, mock_basket = self._mock_ledger_objects(self.invoice_ref)
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        mock_update_payments.return_value = None
        
        # Process payment
        context = self.booking.process_payment_notification(self.invoice_ref)
        
        # Verify AdmissionsBookingInvoice exists
        self.assertTrue(
            AdmissionsBookingInvoice.objects.filter(
                admissions_booking=self.booking,
                invoice_reference=self.invoice_ref
            ).exists()
        )
    
    @patch('mooring.models.Invoice.objects.get')
    @patch('mooring.models.Basket.objects.filter')
    @patch('mooring.models.update_payments')
    def test_process_payment_idempotency(self, mock_update_payments, mock_basket_filter, mock_invoice_get):
        """Test calling twice doesn't duplicate state changes."""
        # Mock ledger objects
        mock_invoice, mock_basket = self._mock_ledger_objects(self.invoice_ref)
        mock_invoice_get.return_value = mock_invoice
        mock_basket_filter.return_value = [mock_basket]
        mock_update_payments.return_value = None
        
        # First call
        context1 = self.booking.process_payment_notification(self.invoice_ref)
        
        # Second call
        context2 = self.booking.process_payment_notification(self.invoice_ref)
        
        # Verify same result
        self.assertEqual(context1['admissionsBooking'].id, context2['admissionsBooking'].id)
        
        # Verify only one invoice record
        self.assertEqual(
            AdmissionsBookingInvoice.objects.filter(admissions_booking=self.booking).count(),
            1
        )

