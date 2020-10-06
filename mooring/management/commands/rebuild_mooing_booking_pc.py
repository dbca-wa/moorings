from django.core.management.base import BaseCommand
from django.utils import timezone
#from mooring.models import RegisteredVessels
from mooring import models
from django.db.models.functions import Length 
from mooring.emails import send_registered_vessels_email
from datetime import datetime
import json

from datetime import timedelta

class Command(BaseCommand):
    help = 'Rebuild mooring booking property cache.'

    def handle(self, *args, **options):

        try:
           bookings = models.Booking.objects.extra(where=["pg_column_size(property_cache) < 12"])[:10]
           for b in bookings:
               print (b.property_cache)
               print ("Rebuilding :"+str(b.id))
               b.update_property_cache()

        except Exception as e:
            print (e)
            #Send fail email
            content = "Error message: {}".format(e)
