"""
URL configuration for medicine project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# project urls.py (replace current content)
from django.contrib import admin
from django.urls import path
from mediflow import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Landing
    path('', views.landing, name='landing'),

    # Donor routes
    path('login/', views.login_view, name='login'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),

    
    path("my-medicines/", views.my_medicines, name="my_medicines"),
    path("pickups/", views.pickups, name="pickups"),
    path("ngo-requests/", views.ngo_requests, name="ngo_requests"),
    path("settings/", views.settings, name="settings"),
    path('add-medicine/', views.add_medicine, name='add_medicine'),

    # NGO routes (namespacing via path names)
    path('NGOlogin/', views.NGOlogin, name='NGOlogin'),
    path('NGOregister/', views.NGOregistration, name='NGOregistration'),
    path('NGOdashboard/', views.NGOdashboard, name='NGOdashboard'),

    # Logout
    path('logout/', views.logout_view, name='logout'),
]
