from django.urls import path

from . import views

app_name = 'security'

urlpatterns = [
    path('', views.index, name='index'),
    path('apps/', views.securityAppsList, name='apps-list'),
    path('add-card/', views.addCard, name='add-card'),
    path('door-stats/', views.get_door_stats, name='door-stats'),
]