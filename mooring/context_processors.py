from django.conf import settings
from django.core.cache import cache
from mooring import models
from mooring import helpers
import json
import hashlib
import uuid
import logging


logger = logging.getLogger(__name__)


def mooring_url(request):
    web_url = request.META.get('HTTP_HOST', None)
    tg = 'pvs'
    if web_url in settings.ROTTNEST_ISLAND_URL:
          tg = 'ria'
    else:
          tg = 'pvs'
    authed = request.user.is_authenticated
    mooring_url = mooring_url_group(tg)

    is_officer = False
    is_inventory = False
    is_admin = False
    is_payment_officer = False
    is_customer = False

    if 'ps_booking' in request.session:
        checkouthash =  hashlib.sha256(str(request.session["ps_booking"]).encode('utf-8')).hexdigest()
        logger.info(f"session['ps_booking']: [{request.session['ps_booking']}] exists.  checkouthash: [{checkouthash}] has been generated from it.")
    else:
        checkouthash = hashlib.sha256(str(uuid.uuid4()).encode('utf-8')).hexdigest()
        logger.info(f"session['ps_booking']: does not exist.  checkouthash: [{checkouthash}] has been generated from uuid.")

    failed_refund_count = 0
    if authed:
         if request.user.is_staff or request.user.is_superuser:
             failed_refund_count = models.RefundFailed.objects.filter(status=0).count()
         is_officer = helpers.is_officer(request.user)
         is_inventory = helpers.is_inventory(request.user)
         is_admin = helpers.is_admin(request.user)
         is_payment_officer = helpers.is_payment_officer(request.user)
         is_customer = helpers.is_customer(request.user)

    mooring_url['REFUND_FAILED_COUNT'] = failed_refund_count
    mooring_url['IS_OFFICER'] = is_officer
    mooring_url['IS_INVENTORY'] = is_inventory
    mooring_url['IS_ADMIN'] = is_admin
    mooring_url['IS_PAYMENT_OFFICER'] = is_payment_officer
    mooring_url['IS_CUSTOMER'] = is_customer
    mooring_url['template_group'] = 'ria'
    mooring_url['checkouthash'] = checkouthash

    return mooring_url
 
#def mooring_url(request):
#    #web_url = request.META['HTTP_HOST']
#    web_url = request.META.get('HTTP_HOST', None)
#    TERMS = ''
#    DAILY_TERMS_URL = ''
#    DAILY_FEES_URL = ''
#    if web_url in settings.ROTTNEST_ISLAND_URL:
#       mooring_group = 'ria'
#       template_group = 'rottnest'
#       alr = None
#       dumped_data = cache.get('AdmissionsLocation:'+mooring_group)
#
#       if dumped_data is None:
#           al= models.AdmissionsLocation.objects.filter(key=mooring_group).values('mooring_booking_terms','daily_admissions_terms','daily_admissions_more_price_info_url')
#           if al.count() > 0:
#              dumped_data = json.dumps(al[0])
#              alr = al[0]
#              cache.set('AdmissionsLocation:'+mooring_group,dumped_data,  3600)
#       else:
#           alr = json.loads(dumped_data)
#           pass
#       if alr:
#          TERMS = alr['mooring_booking_terms']
#          DAILY_TERMS_URL = alr['daily_admissions_terms']
#          DAILY_FEES_URL = alr['daily_admissions_more_price_info_url']
#          #DAILY_TERMS = al[0].daily_admissions_term
#          #TERMS  = "https://www.rottnestisland.com/~/media/Files/boating-documents/marine-hire-facilities-tcs.pdf?la=en"
#       PUBLIC_URL='https://mooring-ria.dbca.wa.gov.au/'
#    else:
#       template_group = 'pvs'
#       mooring_group = 'pvs'
#
#       alr = None
#       dumped_data = cache.get('AdmissionsLocation:'+mooring_group)
#
#       if dumped_data is None:
#           al= models.AdmissionsLocation.objects.filter(key=mooring_group).values('mooring_booking_terms','daily_admissions_terms','daily_admissions_more_price_info_url')
#           if al.count() > 0:
#              dumped_data = json.dumps(al[0])
#              alr = al[0]
#              cache.set('AdmissionsLocation:'+mooring_group,dumped_data,  3600)
#       else:
#           alr = json.loads(dumped_data)
#           pass
#       if alr:
#          TERMS = alr['mooring_booking_terms']
#          DAILY_TERMS_URL = alr['daily_admissions_terms']
#          DAILY_FEES_URL = alr['daily_admissions_more_price_info_url']
#
#       #TERMS = "/know/online-mooring-site-booking-terms-and-conditions"
#       PUBLIC_URL='https://mooring.dbca.wa.gov.au'
#
#
#    is_officer = False
#    is_inventory = False
#    is_admin = False
#    is_payment_officer = False
#    is_customer = False
# 
#    failed_refund_count = 0
#    if request.user.is_authenticated:
#         if request.user.is_staff or request.user.is_superuser:
#             failed_refund_count = models.RefundFailed.objects.filter(status=0).count()
#         is_officer = helpers.is_officer(request.user)
#         is_inventory = helpers.is_inventory(request.user)
#         is_admin = helpers.is_admin(request.user)
#         is_payment_officer = helpers.is_payment_officer(request.user)
#         is_customer = helpers.is_customer(request.user)
#
#    return {
#        'EXPLORE_PARKS_SEARCH': '/map',
#        'EXPLORE_PARKS_CONTACT': '/contact-us',
#        'EXPLORE_PARKS_CONSERVE': '/know/conserving-our-moorings',
#        'EXPLORE_PARKS_PEAK_PERIODS': '/know/when-visit',
#        'EXPLORE_PARKS_ENTRY_FEES': '/know/entry-fees',
#        'EXPLORE_PARKS_TERMS': TERMS,
#        'DAILY_TERMS_URL': DAILY_TERMS_URL,
#        'DAILY_FEES_URL': DAILY_FEES_URL,
#        'PARKSTAY_EXTERNAL_URL': settings.PARKSTAY_EXTERNAL_URL,
#        'DEV_STATIC': settings.DEV_STATIC,
#        'DEV_STATIC_URL': settings.DEV_STATIC_URL,
#        'TEMPLATE_GROUP' : template_group,
#        'GIT_COMMIT_DATE' : settings.GIT_COMMIT_DATE,
#        'GIT_COMMIT_HASH' : settings.GIT_COMMIT_HASH,
#        'SYSTEM_NAME' : settings.SYSTEM_NAME,
#        'REFUND_FAILED_COUNT': failed_refund_count,
#        'IS_OFFICER' : is_officer,
#        'IS_INVENTORY' : is_inventory,
#        'IS_ADMIN' : is_admin,
#        'IS_PAYMENT_OFFICER' : is_payment_officer,
#        'IS_CUSTOMER' : is_customer,
#        'PUBLIC_URL' : PUBLIC_URL,
#        'MOORING_GROUP': mooring_group
#        }



def mooring_url_group(tg):
    #web_url = request.META['HTTP_HOST']
    TERMS = ''
    DAILY_TERMS_URL = ''
    DAILY_FEES_URL = ''
    if tg == 'ria':
       mooring_group = 'ria'
       template_group = 'rottnest'
       alr = None
       dumped_data = cache.get('AdmissionsLocation:'+mooring_group)

       if dumped_data is None:
           al= models.AdmissionsLocation.objects.filter(key=mooring_group).values('mooring_booking_terms','daily_admissions_terms','daily_admissions_more_price_info_url')
           if al.count() > 0:
              dumped_data = json.dumps(al[0])
              alr = al[0]
              cache.set('AdmissionsLocation:'+mooring_group,dumped_data,  3600)
       else:
           alr = json.loads(dumped_data)
           pass
       if alr:
          TERMS = alr['mooring_booking_terms']
          DAILY_TERMS_URL = alr['daily_admissions_terms']
          DAILY_FEES_URL = alr['daily_admissions_more_price_info_url']
          #DAILY_TERMS = al[0].daily_admissions_term
          #TERMS  = "https://www.rottnestisland.com/~/media/Files/boating-documents/marine-hire-facilities-tcs.pdf?la=en"
       PUBLIC_URL='https://mooring-ria.dbca.wa.gov.au/'
    else:
       template_group = 'pvs'
       mooring_group = 'pvs'

       alr = None
       dumped_data = cache.get('AdmissionsLocation:'+mooring_group)

       if dumped_data is None:
           al= models.AdmissionsLocation.objects.filter(key=mooring_group).values('mooring_booking_terms','daily_admissions_terms','daily_admissions_more_price_info_url')
           if al.count() > 0:
              dumped_data = json.dumps(al[0])
              alr = al[0]
              cache.set('AdmissionsLocation:'+mooring_group,dumped_data,  3600)
       else:
           alr = json.loads(dumped_data)
           pass
       if alr:
          TERMS = alr['mooring_booking_terms']
          DAILY_TERMS_URL = alr['daily_admissions_terms']
          DAILY_FEES_URL = alr['daily_admissions_more_price_info_url']

       #TERMS = "/know/online-mooring-site-booking-terms-and-conditions"
       PUBLIC_URL='https://mooring.dbca.wa.gov.au'


#    is_officer = False
#    is_inventory = False
#    is_admin = False
#    is_payment_officer = False
#    is_customer = False
#
#    failed_refund_count = 0
#    if authed:
#         if request.user.is_staff or request.user.is_superuser:
#             failed_refund_count = models.RefundFailed.objects.filter(status=0).count()
#         is_officer = helpers.is_officer(request.user)
#         is_inventory = helpers.is_inventory(request.user)
#         is_admin = helpers.is_admin(request.user)
#         is_payment_officer = helpers.is_payment_officer(request.user)
#         is_customer = helpers.is_customer(request.user)

    return {
        'EXPLORE_PARKS_SEARCH': '/map',
        'EXPLORE_PARKS_CONTACT': '/contact-us',
        'EXPLORE_PARKS_CONSERVE': '/know/conserving-our-moorings',
        'EXPLORE_PARKS_PEAK_PERIODS': '/know/when-visit',
        'EXPLORE_PARKS_ENTRY_FEES': '/know/entry-fees',
        'EXPLORE_PARKS_TERMS': TERMS,
        'DAILY_TERMS_URL': DAILY_TERMS_URL,
        'DAILY_FEES_URL': DAILY_FEES_URL,
        'PARKSTAY_EXTERNAL_URL': settings.PARKSTAY_EXTERNAL_URL,
        'DEV_STATIC': settings.DEV_STATIC,
        'DEV_STATIC_URL': settings.DEV_STATIC_URL,
        'TEMPLATE_GROUP' : template_group,
        'GIT_COMMIT_DATE' : settings.GIT_COMMIT_DATE,
        'GIT_COMMIT_HASH' : settings.GIT_COMMIT_HASH,
        'SYSTEM_NAME' : settings.SYSTEM_NAME,
        'LEDGER_UI_URL' : settings.LEDGER_UI_URL,
        'LEDGER_SYSTEM_ID' : settings.PS_PAYMENT_SYSTEM_ID.replace("S","0"),
#        'REFUND_FAILED_COUNT': failed_refund_count,
#        'IS_OFFICER' : is_officer,
#        'IS_INVENTORY' : is_inventory,
#        'IS_ADMIN' : is_admin,
#        'IS_PAYMENT_OFFICER' : is_payment_officer,
#        'IS_CUSTOMER' : is_customer,
        'PUBLIC_URL' : PUBLIC_URL,
        'MOORING_GROUP': mooring_group
        }



def template_context(request):
    """Pass extra context variables to every template.
    """
    context = mooring_url(request)

    return context



