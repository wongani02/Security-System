from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect

from .forms import UserCardCreationForm
from .models import (
    SecuredDoor, SecurityLog, UserSecurityCredential
)

# Create your views here.


def index(request):

    # Get all doors loaded in the system
    doors = SecuredDoor.objects.all()

    # Get all security logs
    logs = SecurityLog.objects.all().order_by('-created_at')
    successful = logs.filter(entry_status=True)
    declined = logs.filter(entry_status=False)

    # Get all credentioals available
    creds = UserSecurityCredential.objects.all()

    context = {
        'doors': doors,
        'logs': logs,
        'creds': creds,
        'successful': successful,
        'declined': declined,
    }

    if request.htmx:
        return render(request, 'security/partials/table_partial.html', context)
    return render(request, 'security/index.html', context)


def securityAppsList(request):
    
    context = {

    }
    return render(request, 'security/apps-list.html', context)


def addCard(request):

    if request.method == 'POST':
        form = UserCardCreationForm(request.POST)
        if form.is_valid():
            print('valid')
            user_card = UserSecurityCredential.objects.create(
                user=request.user,
                card_uid=form.cleaned_data['rfid_number'],
                card_name=form.cleaned_data['name_on_card']
            )

            for door in form.cleaned_data['doors_to_access']:
                door.permitted_users.add(user_card)

            if request.htmx:
                return render(request, 'security/partials/form-submit.html')
            
            else:
                return HttpResponseRedirect(request.META["HTTP_REFERER"])

    else:
        form = UserCardCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'security/add-card.html', context)


def get_door_stats(request):

    door_id = request.GET.get('door_stats')

    door = get_object_or_404(SecuredDoor, pk=door_id)

    total_scans = SecurityLog.objects.filter(door=door)

    logs = SecurityLog.objects.all().order_by('-created_at')
    successful = total_scans.filter(entry_status=True)
    declined = total_scans.filter(entry_status=False)

    doors = SecuredDoor.objects.all()

    context= {
        'doors': doors,
        'total_door_scans': total_scans,
        'logs': logs,
        'successful': successful,
        'declined': declined,
    }
    return render(request, 'security/partials/door-stats.html', context)