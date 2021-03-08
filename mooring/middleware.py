import re
import datetime

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.utils import timezone
from mooring import utils
from mooring.models import Booking, AdmissionsBooking, BookingAnnualAdmission

CHECKOUT_PATH = re.compile('^/ledger/checkout/checkout')

class BookingTimerMiddleware(object):
    def process_request(self, request):
        #print ("REQUEST SESSION")
        #print request.session['ps_booking']
        print ("LOADING MIDDLE WARE")
        if 'ad_booking' in request.session:
            print ("ADMISSION MIDDLE WARE")
            try:
                booking = AdmissionsBooking.objects.get(pk=request.session['ad_booking'])
            except:
                # no idea what object is in self.request.session['ad_booking'], ditch it
                del request.session['ad_booking']
                return
            if booking.booking_type != 3:
                # booking in the session is not a temporary type, ditch it
                del request.session['ad_booking']
            elif CHECKOUT_PATH.match(request.path) and request.method == 'POST':
                # safeguard against e.g. part 1 of the multipart checkout confirmation process passing, then part 2 timing out.
                # on POST boosts remaining time to at least 2 minutes
                booking.save()

        if 'annual_admission_booking' in request.session:
            print ("ANNUAL ADMISSION MIDDLE WARE")
            try:
                booking = BookingAnnualAdmission.objects.get(pk=request.session['annual_admission_booking'])
            except:
                # no idea what object is in self.request.session['ad_booking'], ditch it
                del request.session['annual_admission_booking']
                return
            if booking.booking_type != 3:
                # booking in the session is not a temporary type, ditch it
                del request.session['annual_admission_booking']
            elif CHECKOUT_PATH.match(request.path) and request.method == 'POST':
                # safeguard against e.g. part 1 of the multipart checkout confirmation process passing, then part 2 timing out.
                # on POST boosts remaining time to at least 2 minutes
                booking.save()
            print ("END ANNUAL")
        if 'ps_booking' in request.session:
            print ("YES PS BOOKING")
            print (request.session['ps_booking'])
        #    print ("BOOKING SESSION : "+str(request.session['ps_booking']))
            try:
                booking = Booking.objects.get(pk=request.session['ps_booking'])
            except:
                # no idea what object is in self.request.session['ps_booking'], ditch it
                del request.session['ps_booking']
                return
            if booking.booking_type != 3:
                # booking in the session is not a temporary type, ditch it
                del request.session['ps_booking']
            elif timezone.now() > booking.expiry_time:
                # expiry time has been hit, destroy the Booking then ditch it
                #booking.delete()
                del request.session['ps_booking']
            elif CHECKOUT_PATH.match(request.path) and request.method == 'POST':
                # safeguard against e.g. part 1 of the multipart checkout confirmation process passing, then part 2 timing out.
                # on POST boosts remaining time to at least 2 minutes
                booking.expiry_time = max(booking.expiry_time, timezone.now()+datetime.timedelta(minutes=3))
                booking.save()

        if CHECKOUT_PATH.match(request.path):
            basket = utils.get_basket(request)
            booking_reference = basket.booking_reference
            print (booking_reference[:2])
            if booking_reference[:2] == 'PS':
                   booking_id = booking_reference.split("-")
                   print ("parkstay booking")
                   try:
                       del request.session['ad_booking']
                       del request.session['annual_admission_booking']
                   except:
                       pass
                   booking = Booking.objects.get(pk=int(booking_id[1]))
                   if timezone.now() > booking.expiry_time:
                       try:
                           del request.session['ps_booking']
                       except:
                           pass
                       return HttpResponseRedirect(reverse('public_make_booking'))

        # force a redirect if in the checkout
        if ('ps_booking_internal' not in request.COOKIES) and CHECKOUT_PATH.match(request.path):
            if ('ps_booking' not in request.session) and CHECKOUT_PATH.match(request.path) and ('ad_booking' not in request.session) and ('annual_admission_booking' not in request.session):
                return HttpResponseRedirect(reverse('public_make_booking'))
            else:
                return
            return HttpResponseRedirect(reverse('public_make_booking'))
        return
