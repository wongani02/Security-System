from django import template
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from security.models import (
    SecuredDoor, SecurityLog
)

register = template.Library()

@register.simple_tag
def get_total_door_scans(arg):

    door = get_object_or_404(SecuredDoor, pk=arg)

    total_scans = SecurityLog.objects.filter(door=door)

    return total_scans.count()


@register.simple_tag
def get_total_failed_door_scans(arg):

    door = get_object_or_404(SecuredDoor, pk=arg)

    total_scans = SecurityLog.objects.filter(door=door, entry_status=False)

    return total_scans.count()


@register.simple_tag
def get_total_success_door_scans(arg):

    door = get_object_or_404(SecuredDoor, pk=arg)

    total_scans = SecurityLog.objects.filter(door=door, entry_status=True)

    return total_scans.count()




