import logging
from mooring import settings
from ledger_api_client.managed_models import SystemGroup


logger = logging.getLogger(__name__)


class DefaultDataManager(object):
    def __init__(self):
        for group_name in settings.GROUP_NAME_CHOICES:
            try:
                group, created = SystemGroup.objects.get_or_create(name=group_name)
                if created:
                    logger.info(f"SystemGroup: [{group}] has been created.")
                else:
                    logger.debug(f"SystemGroup: [{group}] already exists.")
            except Exception as e:
                logger.error(f"{e}, SystemGroup: [{group_name}]")
