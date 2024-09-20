from django.core.management.base import BaseCommand
from django.utils import timezone
from mooring.models import GlobalSettings, MooringAreaGroup
# from ledger.payments.bpoint.models import BpointTransaction, BpointToken
# from ledger.payments.models import Invoice,OracleInterface,CashTransaction
# from ledger.order.models import Order
from ledger_api_client.ledger_models import Invoice
from ledger_api_client.order import Order
from django.core.exceptions import ValidationError
from django.conf import settings
from decimal import *
from mooring.emails import sendHtmlEmail
import json

from datetime import timedelta, datetime

class Command(BaseCommand):
    help = 'Check BPOINT Settlement dates with oracle Invoice Settlement dates to ensure totals match.'

    def handle(self, *args, **options):
            bpoint_total = Decimal('0.00')
            oracle_total = Decimal('0.00')
            invoice_total = Decimal('0.00')
            yesterday = datetime.today() - timedelta(days=1)
            today = datetime.today()# - timedelta(days=41)
            tomorrow = datetime.today() + timedelta(days=1)

            system = settings.PS_PAYMENT_SYSTEM_ID
            system = system.replace('S','0')
            bpoint_array = {}
            invoice_array ={}
            mismatch_bpoint = []
            mismatch_invoice = []
            ba_missing = []
            ia_missing = []
            dates_to_check = [yesterday,today,tomorrow]

            print (system)
            try:
                 for settlement_date in dates_to_check:
                     print ("Settlement Date: "+str(settlement_date.strftime("%d/%m/%Y")))
                     bpoint_total = Decimal('0.00')
                     oracle_total = Decimal('0.00')
                     invoice_total = Decimal('0.00')
                     bpoint_array = {}
                     invoice_array ={}
                     mismatch_bpoint = []
                     mismatch_invoice = []
                     ba_missing = []
                     ia_missing = []


                     
                     print ("Calculation Bpoint Transaction Total")
                     bpoint_trans = BpointTransaction.objects.filter(settlement_date=settlement_date, crn1__istartswith=system)
                     for i in bpoint_trans:
                          tran_total = Decimal('0.00')
                          if i.action == 'payment':
                                  bpoint_total = bpoint_total + Decimal(i.amount)
                                  tran_total = Decimal(i.amount)
                          if i.action == 'refund':
                                  bpoint_total = bpoint_total - Decimal(i.amount)
                                  tran_total =  tran_total - Decimal(i.amount) 
                          bpoint_array[i.crn1] = tran_total 

                     print (bpoint_total)
                     print ("Calculation Invoice Settlemnt Oracle Totals")

                     invoices = Invoice.objects.filter(settlement_date=settlement_date)
                     for i in invoices:
                         #print (i.reference)
                         invoice_total = invoice_total + Decimal(i.amount)
                         #print (i.order)
                         trans_order_total = Decimal('0.00')
                         for ol in Order.objects.get(number=i.order_number).lines.all():
                              for order_total in ol.payment_details['order']:
                                  oracle_total = oracle_total + Decimal(ol.payment_details['order'][order_total])
                                  trans_order_total = trans_order_total + Decimal(ol.payment_details['order'][order_total])
                                  #print (Decimal(ol.payment_details['order'][order_total]))
                                  #print (oracle_total)
                              invoice_array[i.reference] = trans_order_total 
                     print ("ORACLE TOTAL")
                     print (oracle_total)
                     print (invoice_total)
                     #bpoint with mismatching invoice
                     for ba in bpoint_array:
                         if ba in invoice_array:
                             if bpoint_array[ba] != invoice_array[ba]:
                                  mismatch_bpoint.append('Mismatch: '+ba+'('+invoice_array[ba]+')'+'('+bpoint_array[ba]+')')
                             else:
                                  ba_missing.append('BP No exist: '+ba+'('+str(bpoint_array[ba])+')')

                     # invoice with mismatching bpoint
                     for ia in invoice_array:
                         #print (ia)
                         #print (invoice_array[ia])
                         if ia in bpoint_array:
                             #print (bpoint_array[ia])
                             if invoice_array[ia] != bpoint_array[ia]:
                                 mismatch_invoice.append('Mismatch: '+ia+'('+invoice_array[ia]+')'+'('+bpoint_array[ia]+')')
                             else:
                                 ia_missing.append(ia+'('+str(invoice_array[ia])+')')
                     
                     if bpoint_total != oracle_total:
                          print ("Sending Report")
                          context = {
                                'error_report': "Bpoint and Oracle Totals do not match. Bpoint Total: "+str(bpoint_total)+" Oracle Total: "+str(oracle_total),
                     'mismatch_bpoint': mismatch_bpoint,
                     'mismatch_invoice' : mismatch_invoice,
                     'ba_missing': ba_missing,
                     'ia_missing': ia_missing,
                     'settlement_date': settlement_date

                          }
                          email_list = []
                          for email_to in settings.NOTIFICATION_EMAIL.split(","):
                              email_list.append(email_to)
                          sendHtmlEmail(tuple(email_list),"[MOORING] oracle and bpoint total mistatch",context,'mooring/email/oracle_bpoint_report.html',None,None,settings.EMAIL_FROM,'system-oim',attachments=None)
                          #raise ValidationError("Bpoint and Oracle Totals do not match. Bpoint Total: "+str(bpoint_total)+" Oracle Total: "+str(oracle_total))
            except Exception as e:
                 print ("Error: Sending Email Notification: "+settings.NOTIFICATION_EMAIL)
                 context = {
                     'error_report' : str(e),
                 }
                 email_list = []
                 for email_to in settings.NOTIFICATION_EMAIL.split(","):
                        email_list.append(email_to)
                 sendHtmlEmail(tuple(email_list),"[MOORING] oracle and bpoint total mistatch",context,'mooring/email/oracle_bpoint.html',None,None,settings.EMAIL_FROM,'system-oim',attachments=None)



