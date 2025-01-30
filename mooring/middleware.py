import re
import datetime
import logging
from django.contrib import messages

#from django.core.urlresolvers import reverse
from django.urls import reverse
from django.http import Http404, HttpResponse, JsonResponse, HttpResponseRedirect
from django.utils import timezone
from mooring.models import AdmissionsBooking, Booking, BookingAnnualAdmission
import hashlib

from mooring.utils import delete_session_booking


logger = logging.getLogger(__name__)

class CacheHeaders(object):
    # def process_response(self, request, response):
    #      if request.path[:5] == '/api/':
    #           response['Cache-Control'] = 'private, no-store'
    #      return response
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/api/'):
            response['Cache-Control'] = 'private, no-store'
        return response


CHECKOUT_PATH = re.compile('^/ledger-api')
PROCESS_PAYMENT =  re.compile('^/ledger-api/process-payment')

# class BookingTimerMiddleware(object):

#     def __init__(self, get_response):            
#             self.get_response = get_response

#     def process_view(self, request, view_func, view_args, view_kwargs):
#         # Run before executing any function code

#         if 'ps_booking' in request.session:               
#                if request.path.startswith("/ledger-api/process-payment") or request.path.startswith('/ledger-api/payment-details'):                                       
#                     checkouthash =  hashlib.sha256(str(request.session["ps_booking"]).encode('utf-8')).hexdigest()
#                     checkouthash_cookie = request.COOKIES.get('checkouthash')
#                     print ("MIDDLE 1")
#                     print (request.session['ps_booking'])
#                     print (checkouthash_cookie)
#                     print (checkouthash)
#                     total_booking = Booking.objects.filter(pk=request.session['ps_booking']).count()
#                     if checkouthash_cookie != checkouthash or total_booking == 0:                         
#                          # messages.error(request, "There was a booking mismatch issue while trying to complete your booking, your inprogress booking has been cancelled and will need to be completed again.  This can sometimes be caused by using multiple browser tabs and recommend only to complete a booking using one browser tab window. ")          
#                          # return HttpResponseRedirect("/")  
#                          print ("MIDDLE 2")
#                          url_redirect = reverse('public_make_booking')
#                          response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
#                          return response          

#         else:
#                if request.path.startswith("/ledger-api/process-payment"):
#                     # booking as expired or session been removed
#                     url_redirect = reverse('public_make_booking')
#                     response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
#                     return response             
#         return None

#     def __call__(self, request):            
#             # Run after executing any function code
#             return self.pr(request)

#     def pr(self, request):
#         response= self.get_response(request)
#         if request.path.startswith('/static') or request.path.startswith('/favicon') or request.path.startswith('/media') or request.path.startswith('/api') or request.path.startswith('/search-availability/information/') or request.path.startswith('/search-availability/campground/') or request.path.startswith('/campground-image') or request.path == '/':
#              pass
#         else:
#             if 'ps_booking' in request.session:
#                 try:
#                     booking = Booking.objects.get(pk=request.session['ps_booking'])
#                 except:
#                     # no idea what object is in self.request.session['ps_booking'], ditch it
#                     del request.session['ps_booking']
#                     return response
#                 #if booking.booking_type != 3:
#                 #    # booking in the session is not a temporary type, ditch it
#                 #    del request.session['ps_booking']
#                 if booking.expiry_time is not None:
#                     if timezone.now() > booking.expiry_time and booking.booking_type == 3:
#                     # expiry time has been hit, destroy the Booking then ditch it
#                     #booking.delete()
#                         del request.session['ps_booking']

#                 if request.path.startswith("/ledger-api/process-payment") or request.path.startswith('/ledger-api/payment-details'):      
                    
#                     if "ps_booking" not in request.session:
#                          url_redirect = reverse('public_make_booking')
#                          response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
#                          return response    

#                     checkouthash =  hashlib.sha256(str(request.session["ps_booking"]).encode('utf-8')).hexdigest() 

#                     checkouthash_cookie = request.COOKIES.get('checkouthash')
#                     total_booking = Booking.objects.filter(pk=request.session['ps_booking']).count()
#                     if checkouthash_cookie != checkouthash or total_booking == 0:                         
#                          # messages.error(request, "There was a booking mismatch issue while trying to complete your booking, your inprogress booking has been cancelled and will need to be completed again.  This can sometimes be caused by using multiple browser tabs and recommend only to complete a booking using one browser tab window. ")          
#                          # return HttpResponseRedirect("/")  
#                          url_redirect = reverse('public_make_booking')
#                          response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
#                          return response                                                                                                 

#                 if CHECKOUT_PATH.match(request.path) and request.method == 'POST' and booking.booking_type == 3:
#                     # safeguard against e.g. part 1 of the multipart checkout confirmation process passing, then part 2 timing out.
#                     # on POST boosts remaining time to at least 2 minutes
#                     booking.expiry_time = max(booking.expiry_time, timezone.now()+datetime.timedelta(minutes=2))
#                     booking.save()
#             else:
#                  if request.path.startswith("/ledger-api/process-payment"):
#                     # booking as expired or session been removed
#                     url_redirect = reverse('public_make_booking')
#                     response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
#                     return response

#             # force a redirect if in the checkout
#             if ('ps_booking_internal' not in request.COOKIES) and CHECKOUT_PATH.match(request.path):
#                 if ('ps_booking' not in request.session) and CHECKOUT_PATH.match(request.path):
#                     url_redirect = reverse('public_make_booking')
#                     response = HttpResponse("<script> window.location='"+url_redirect+"';</script> <center><div class='container'><div class='alert alert-primary' role='alert'><a href='"+url_redirect+"'> Redirecting please wait: "+url_redirect+"</a><div></div></center>")
#                     return response
#                     #return HttpResponseRedirect(reverse('public_make_booking'))
#                 else:
#                     return response
#         return response



class BookingTimerMiddleware(object):
    def __init__(self, get_response):            
            self.get_response = get_response

    def process_view(self, request, view_func, view_args, view_kwargs):
        logger.info("in BookingTimerMiddleware.process_view()...")
        if 'ad_booking' in request.session:
            logger.info(f"session['ad_booking']: [{request.session['ad_booking']}] exists.")
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
        else:
            logger.info('session[ad_booking] does not exist.')

        if 'annual_admission_booking' in request.session:
            logger.info(f"session['annual_admission_booking']: [{request.session['annual_admission_booking']}] exists.")
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
        else:
            logger.info(f'session[annual_admission_booking] does not exist.')

        if 'ps_booking' in request.session:
            logger.info(f"session['ps_booking']: [{request.session['ps_booking']}] exists.")

            # TEST
            checkouthash =  hashlib.sha256(str(request.session["ps_booking"]).encode('utf-8')).hexdigest()
            checkouthash_cookie = request.COOKIES.get('checkouthash')
            if checkouthash_cookie != checkouthash:
                logger.info(f"***** checkouthash mismatch: [{checkouthash}] != [{checkouthash_cookie}]")
            else:
                logger.info(f"***** checkouthash match: [{checkouthash}] == [{checkouthash_cookie}]")
            # END TEST

            try:
                booking = Booking.objects.get(pk=request.session['ps_booking'])
            except:
                # no idea what object is in self.request.session['ps_booking'], ditch it
                delete_session_booking(request.session)
                return

            if booking.booking_type != 3:
                # booking in the session is not a temporary type, ditch it
                delete_session_booking(request.session)
            elif timezone.now() > booking.expiry_time:
                # expiry time has been hit, destroy the Booking then ditch it
                #booking.delete()
                delete_session_booking(request.session)
            elif CHECKOUT_PATH.match(request.path) and request.method == 'POST':
                # safeguard against e.g. part 1 of the multipart checkout confirmation process passing, then part 2 timing out.
                # on POST boosts remaining time to at least 2 minutes
                booking.expiry_time = max(booking.expiry_time, timezone.now()+datetime.timedelta(minutes=3))
                booking.save()
        else:
            logger.info('session[ps_booking] does not exist.')

        if CHECKOUT_PATH.match(request.path):
            booking = Booking.objects.get(pk=request.session['ps_booking'])
            booking_reference = 'PS' + str(booking.id)
            if booking_reference[:2] == 'PS':
                booking_id = booking_reference.split("-")
                try:
                    del request.session['ad_booking']
                    del request.session['annual_admission_booking']
                except:
                    pass
                if timezone.now() > booking.expiry_time:
                    try:
                        delete_session_booking(request.session)
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

    def __call__(self, request):            
            # Run after executing any function code
            return self.pr(request)

    def pr(self, request):
        response= self.get_response(request)
        return response
