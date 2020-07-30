from django.core.management.base import BaseCommand
from django.utils import timezone
#from mooring.models import RegisteredVessels
from mooring import models
from mooring.emails import send_registered_vessels_email
from datetime import datetime
import json

from datetime import timedelta

class Command(BaseCommand):
    help = 'Import vessels from RegisteredVessels into VesselDetail table (RegisteredVessels is a daily since from lotus notes).'

    def handle(self, *args, **options):

        try:
           rv = models.RegisteredVessels.objects.all()
           for r in rv:
                if models.VesselDetail.objects.filter(rego_no=r.rego_no).count() > 0:
                     print ("Skipping: "+r.rego_no)
                else:
                    print ("Creating: "+r.rego_no)
                    models.VesselDetail.objects.create(rego_no=r.rego_no,
                                                       vessel_size=r.vessel_size,
                                                       vessel_draft=r.vessel_draft,
                                                       vessel_beam=r.vessel_beam,
                                                       vessel_weight=r.vessel_weight
                                                      )


        except Exception as e:
            print (e)
            #Send fail email
            content = "Error message: {}".format(e)
            send_registered_vessels_email(content)
