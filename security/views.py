from django.shortcuts import render

from .models import (
    SecuredDoor, SecurityLog, UserSecurityCredential
)

# Create your views here.


def index(request):

    # Get all doors loaded in the system
    doors = SecuredDoor.objects.all()

    # Get all security logs
    logs = SecurityLog.objects.all()
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
    return render(request, 'security/index.html', context)


def securityAppsList(request):
    
    context = {

    }
    return render(request, 'security/apps-list.html', context)


def addCard(request):

    context = {

    }
    return render(request, 'security/add-card.html', context)