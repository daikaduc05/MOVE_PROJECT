"""
URL configuration for Move_Ex project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from django.urls import include
from .views import Register,Active,SendEmail,Login,ChangePassword
urlpatterns = [
    path('api/auth/register',Register.as_view(),name = 'api_register'),
    path('api/auth/active', Active.as_view(), name="api_active"),
    path('api/send_email', SendEmail.as_view(), name="api_send_email"),
    path('api/auth/login',Login.as_view(),name="api_login"),
    path('api/auth/change_password',ChangePassword.as_view(),name = "api_change_password"),
    
]
