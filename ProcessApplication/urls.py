"""
URL configuration for Main project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from LoginManager.views import loginuser
from . import views

urlpatterns = [
    path('application_List', views.application_List, name="application_List"),
    path('ApproveApplication/<int:applicationId>', views.ApproveApplication, name="ApproveApplication"),
    path('DeclineApplication/<int:applicationId>', views.DeclineApplication, name="DeclineApplication"),
    path('CancelApplication/<int:applicationId>', views.CancelApplication, name="CancelApplication"),
    path('addApparel/<int:applicationId>', views.addApparel, name="addApparel"),
    path('noLetterActivate/<int:applicationId>', views.noLetterActivate, name="noLetterActivate"),
    
    path('approveApplicant', views.approveApplicant, name="approveApplicant"),
    path('declineApplicant', views.declineApplicant, name="declineApplicant"),
    path('declineApplicant_committee/<int:applicantApplicationId>', views.declineApplicant_committee, name="declineApplicant_committee")
    
    
]
