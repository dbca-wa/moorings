from django.core.management.base import BaseCommand
from django.utils import timezone
from mooring.models import GlobalSettings, MooringAreaGroup
from ledger.payments.bpoint.models import BpointTransaction, BpointToken
from ledger.payments.models import Invoice,OracleInterface,CashTransaction
from oscar.apps.order.models import Order
from django.core.exceptions import ValidationError
from django.conf import settings
from decimal import *
from mooring.emails import sendHtmlEmail
import json

from datetime import timedelta, datetime

class Command(BaseCommand):
    help = 'Check for bpoint transaction with missing bookings.'

    def handle(self, *args, **options):
            bpoint_total = Decimal('0.00')
            oracle_total = Decimal('0.00')
            invoice_total = Decimal('0.00')
            today = datetime.today()# - timedelta(days=3)
            fiveminutesago = datetime.now() - timedelta(minutes=5)
            system = settings.PS_PAYMENT_SYSTEM_ID
            system = system.replace('S','0')
            print (system)
            try:
                 print ("Calculation Bpoint Transaction Total")
                 bpoint_trans = BpointTransaction.objects.filter(created__gte=fiveminutesago, crn1__startswith=settings.PS_PAYMENT_SYSTEM_ID)
                 for i in bpoint_trans:
                         print (i)

            except Exception as e:
                 print ("Error: Sending Email Notification: "+settings.NOTIFICATION_EMAIL)
                 context = {
                     'error_report' : str(e)
                 }
                 email_list = []
                 for email_to in settings.NOTIFICATION_EMAIL.split(","):
                        email_list.append(email_to)
                 sendHtmlEmail(tuple(email_list),"[MOORING] oracle and bpoint total mistatch",context,'mooring/email/oracle_bpoint.html',None,None,settings.EMAIL_FROM,'system-oim',attachments=None)



