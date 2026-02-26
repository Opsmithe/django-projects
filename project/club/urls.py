from django.urls import path
from . import views

app_name = 'club'

urlpatterns = [
   path('', views.main, name='main'),
   path('members/', views.members, name='members'),
   path('member/<slug:slug>/', views.details, name='member-detail'),
   path('testing/', views.testing, name='testing')
]
