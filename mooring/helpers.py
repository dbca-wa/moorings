from __future__ import unicode_literals
# from ledger.accounts.models import EmailUser
from ledger_api_client.ledger_models import EmailUserRO
from django.core.cache import cache
from ledger_api_client.managed_models import SystemGroup, SystemGroupPermission


def belongs_to(user, group_name):
    """
    Check if the user belongs to the given group.
    :param user:
    :param group_name:
    :return:
    """
    # return user.groups.filter(name=group_name).exists()
    belongs_to_value = cache.get('User-belongs_to'+str(user.id)+'group_name:'+group_name)
    #belongs_to_value = None
    if belongs_to_value:
        print ('From Cache - User-belongs_to'+str(user.id)+'group_name:'+group_name)
    if belongs_to_value is None:
       sg = SystemGroup.objects.filter(name=group_name)
       if sg.count() > 0:
          sgp = SystemGroupPermission.objects.filter(system_group=sg[0],emailuser=user)
          if sgp.count() > 0:
               belongs_to_value = True
          #belongs_to_value = SystemGroup.object.filter(name=group_name).exists()
       cache.set('User-belongs_to'+str(user.id)+'group_name:'+group_name, belongs_to_value, 3600)
    return belongs_to_value


def is_officer(user):
    return user.is_authenticated and user.is_staff

def is_inventory(user):
    return user.is_authenticated and belongs_to(user, "Mooring Inventory")

def is_admin(user):
    return user.is_authenticated and belongs_to(user, "Mooring Admin")

def is_payment_officer(user):
    return user.is_authenticated and belongs_to(user, "Payments Officers")

def is_customer(user):
    """
    Test if the user is a customer
    Rules:
        Not an officer
    :param user:
    :return:
    """
    return user.is_authenticated and not is_officer(user)


def get_all_officers():
    # return EmailUser.objects.filter(is_staff=True)
    return EmailUserRO.objects.filter(is_staff=True)

def can_view_campground(user,campground):
    for g in campground.mooringareagroup_set.all():
        if user in g.members.all():
            return True
    return False
