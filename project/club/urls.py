from django.urls import path
from . import views
from . import auth_views

app_name = 'club'

urlpatterns = [
   # Main pages
   path('', views.main, name='main'),
   path('members/', views.members, name='members'),
   path('member/create/', views.create_member, name='create-member'),
   path('member/<slug:slug>/', views.details, name='member-detail'),
   path('member/<slug:slug>/edit/', views.edit_member, name='edit-member'),
   path('member/<slug:slug>/delete/', views.delete_member, name='delete-member'),
   path('testing/', views.testing, name='testing'),
   
   # Authentication URLs
   path('register/', auth_views.register_view, name='register'),
   path('login/', auth_views.login_view, name='login'),
   path('logout/', auth_views.logout_view, name='logout'),
   path('profile/', auth_views.profile_view, name='profile'),
]
