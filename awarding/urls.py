
from django.contrib import admin
from django.urls import path
from . import views



urlpatterns = [
    path('ApprovedApplications', views.ApprovedApplications,  name="ApprovedApplications" ),
    path('awardingColors/<int:applicationId>', views.awardingColors, name="awardingColors")
]
