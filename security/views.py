from django.shortcuts import render

# Create your views here.


def index(request):


    context = {

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