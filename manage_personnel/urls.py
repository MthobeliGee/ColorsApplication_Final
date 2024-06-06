from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path('new_personnel', views.new_personnel, name="new_personnel"),
    path('getFederation', views.getFederation, name="getFederation"),
    path('colorControl/<str:federationName>', views.colorControl, name="colorControl"),
]