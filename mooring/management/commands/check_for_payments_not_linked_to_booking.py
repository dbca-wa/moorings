from django.core.management.base import BaseCommand
from django.utils import timezone
from mooring.emails import sendHtmlEmail
from mooring import models 
from mooring import utils
from mooring import context_processors
#from ledger.payments.bpoint.models import BpointTransaction, BpointToken
#from ledger.payments.models import Invoice,OracleInterface,CashTransaction
#from ledger.order.models import Order
from ledger.basket.models import Basket
from django.conf import settings
from datetime import timedelta, datetime
from ledger.payments.utils import bpoint_integrity_checks, bpoint_integrity_checks_completed

class Command(BaseCommand):
    help = 'Check for payment which have been completed but are missing a booking.'

    def handle(self, *args, **options):
           rows = []
           system = settings.PS_PAYMENT_SYSTEM_ID
           system = system.replace('S','0')
           rows = bpoint_integrity_checks(system,2,10)

           for r in rows:
               print (r['booking_reference'])
               print (r)
               booking_reference_split = r['booking_reference'].split('-')
               if len(booking_reference_split) == 2:
                   booking_group_type= booking_reference_split[0]
                   booking_id = booking_reference_split[1]

                   if booking_group_type == 'AA':
                       baa = models.BookingAnnualAdmission.objects.filter(id=booking_id)
                       basket = Basket.objects.filter(id=int(r['basket']))
                       if baa.count() > 0:
                           pass
                           if baa[0].booking_type == 3:
                              baa[0].annual_booking_period_group.mooring_group
                              mooring_group_id = baa[0].annual_booking_period_group.mooring_group.id
                              al = models.AdmissionsLocation.objects.get(mooring_group__id=mooring_group_id)
                              cp = context_processors.mooring_url_group(al.key)
                              context = utils.booking_annual_admission_success(basket, baa[0], cp)
                              bpoint_integrity_checks_completed(r['bpoint_id'],r['reference'])

                              emails = models.EmailGroup.objects.filter(email_group=1, mooring_group=mooring_group_id)
                              context = {
                                  'booking' : baa[0],
                                  'booking_reference': r['booking_reference'].replace("-",""),
                                  'invoice': r['reference'],
                                  'customer_name': baa[0].details['first_name']+' '+baa[0].details['last_name']

                              }
                              email_list = []
                              for e in emails:
                                  email_list.append(e.email)
                              sendHtmlEmail(tuple(email_list),"[MOORING] Annual Admission Booking Recovery for ("+str(r['booking_reference'].replace("-",""))+") with invoice ("+r['reference']+")",context,'mooring/email/booking_recovery.html',None,None,settings.EMAIL_FROM,'system-oim',attachments=None)

                              print ("AA")
                              print (baa[0].id)
                           else:
                               bpoint_integrity_checks_completed(r['bpoint_id'],r['reference'])
                   if booking_group_type == 'AD':
                       baa = models.AdmissionsBooking.objects.filter(id=booking_id)
                       basket = Basket.objects.filter(id=int(r['basket']))
                       
                       if baa.count() > 0:
                           pass
                           if baa[0].booking_type == 3:
                              al = models.AdmissionsLine.objects.filter(admissionsBooking=baa[0]) 
                              cp = context_processors.mooring_url_group(al[0].location.key)
                              context = utils.booking_admission_success(basket, baa[0], cp)
                              print ("AD")
                              print (baa[0].id)
                              bpoint_integrity_checks_completed(r['bpoint_id'],r['reference'])
                              print ("Sending Email")
                              emails = models.EmailGroup.objects.filter(email_group=2, mooring_group=al[0].location.mooring_group.id)
                              context = {
                                  'booking' : baa[0],
                                  'booking_reference': r['booking_reference'].replace("-",""),
                                  'invoice': r['reference'],
                                  'customer_name': baa[0].customer
                              }

                              email_list = []
                              for e in emails:
                                  email_list.append(e.email)
                              sendHtmlEmail(tuple(email_list),"[MOORING] Admission Booking Recovery for ("+str(r['booking_reference'].replace("-",""))+") with invoice ("+r['reference']+")",context,'mooring/email/booking_recovery.html',None,None,settings.EMAIL_FROM,'system-oim',attachments=None)
                           else:
                              bpoint_integrity_checks_completed(r['bpoint_id'],r['reference'])



                   if booking_group_type == 'PS':
                       baa = models.Booking.objects.filter(id=booking_id)
                       if baa.count() > 0:
                           basket = Basket.objects.filter(id=int(r['basket']))
                           if baa[0].mooringarea:
                               if baa[0].booking_type == 3:
                                  
                                  mg = models.MooringAreaGroup.objects.filter(moorings__in=[baa[0].mooringarea.id])
                                  al = models.AdmissionsLocation.objects.get(mooring_group__id=mg[0].id)
                                  cp = context_processors.mooring_url_group(al.key)
                                  context = utils.booking_success(basket, baa[0], cp)
                                  bpoint_integrity_checks_completed(r['bpoint_id'],r['reference'])
                                  emails = models.EmailGroup.objects.filter(email_group=1, mooring_group=mg[0])
                                  context = {
                                      'booking' : baa[0],
                                      'booking_reference': r['booking_reference'].replace("-",""),
                                      'invoice': r['reference'],
                                      'customer_name' : baa[0].details['first_name']+' '+baa[0].details['last_name']
                                  }

                                  email_list = []
                                  for e in emails:
                                      email_list.append(e.email)
                                  sendHtmlEmail(tuple(email_list),"[MOORING] Booking Recovery for ("+str(r['booking_reference'].replace("-",""))+") with invoice ("+r['reference']+")",context,'mooring/email/booking_recovery.html',None,None,settings.EMAIL_FROM,'system-oim',attachments=None)
                               else:
                                   bpoint_integrity_checks_completed(r['bpoint_id'],r['reference'])
               else:                       
                   bpoint_integrity_checks_completed(r['bpoint_id'],r['reference'])



