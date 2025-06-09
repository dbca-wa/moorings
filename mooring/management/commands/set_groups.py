from django.core.management.base import BaseCommand
from ledger_api_client.managed_models import SystemGroup
from mooring.models import MooringAreaGroup
from settings import GROUP_NAME_MOORING_ADMIN, GROUP_NAME_MOORING_INVENTORY, GROUP_NAME_PAYMENTS_OFFICERS


class Command(BaseCommand):
    help = 'Set auth groups.'

    def handle(self, *args, **options):
        if not SystemGroup.objects.filter(name=GROUP_NAME_MOORING_ADMIN).count() > 0:
            SystemGroup.objects.create(name=GROUP_NAME_MOORING_ADMIN)
        if not SystemGroup.objects.filter(name=GROUP_NAME_MOORING_INVENTORY).count() > 0:
            SystemGroup.objects.create(name=GROUP_NAME_MOORING_INVENTORY)
        if not SystemGroup.objects.filter(name=GROUP_NAME_PAYMENTS_OFFICERS).count() > 0:
            SystemGroup.objects.create(name=GROUP_NAME_PAYMENTS_OFFICERS)
        if not MooringAreaGroup.objects.filter(name="Rottnest Island Authority").count() > 0:
            MooringAreaGroup.objects.create(name="Rottnest Island Authority")
        if not MooringAreaGroup.objects.filter(name="Parks and Wildlife").count() > 0:
            MooringAreaGroup.objects.create(name="Parks and Wildlife")