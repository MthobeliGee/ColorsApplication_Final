from django.shortcuts import render
from django.shortcuts import render,redirect, get_object_or_404
from MyApp.models import *
from MyApp.views import AlertGovManager
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from datetime import datetime
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
import requests

from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse



@login_required
def new_personnel(request):
    
    user = request.user
    
    if request.method =='GET':
       
        return render(request, 'manage_personnel/new_personnel.html')
    
    
    
    if request.method == 'POST':
        
        personnel = FederationPersonel.objects.create(
            user = request.user,
            first_name = request.POST["first_name"],
            last_name = request.POST["last_name"],
            id_number = request.POST["id_number"],
            Gender = request.POST["Gender"],
            email = request.POST["email"],
            Phone = request.POST["Phone"],
           
            
        ) 
    return redirect("getFederation")



def getFederation(request):
    
    # try:
   
    #    # url = 'https://yonelahopewell1.pythonanywhere.com/GovApisComplayingFederations'
    #     url = 'https://kznsannualreport.pythonanywhere.com/GovApisComplayingFederations'
    #     r = requests.get(url)
    
     
    #     data = r.json()
        
    #     print()
    #     federations = data["federations"]
    #     #print("The request data fed list: ", data["federations"][0]["federationName"])
    # except :
    #     pass
    if request.method == 'GET':
        federations =[
            {
                "federationName":"KZN AQUATICS",
                "userName":"Yonela",
                "userSurname":"Sitshaka",
                "userEmail":"livesoundsmusic@gmail.com"

            },
            {
                "federationName":"SAFA",
                "userName":"Hopewell",
                "userSurname":"Sitshaka",
                "userEmail":"yonela@kznsc.com"

            },
            {
                "federationName":"SAFA2",
                "userName":"Hopewell",
                "userSurname":"Sitshaka",
                "userEmail":"yonela@kznsc.com"

            },
            {
                "federationName":"SAFA3",
                "userName":"Hopewell",
                "userSurname":"Sitshaka",
                "userEmail":"yonela@kznsc.com"

            },
            {
                "federationName":"SAFA4",
                "userName":"Hopewell",
                "userSurname":"Sitshaka",
                "userEmail":"yonela@kznsc.com"

            },
            {
                "federationName":"SAFA5",
                "userName":"Hopewell",
                "userSurname":"Sitshaka",
                "userEmail":"yonela@kznsc.com"

            }
        ]
        for fed in federations:
            try:
                ff = get_object_or_404(Federation, FederationName =fed.federationName )
                if ff:
                    federations.remove(ff)
            except:
                pass
    
    

        return render(request,  'MyApp/federations.html',{"federations":filterFederations(federations)})
    
    if request.method == 'POST':
        
        user=  request.user
        FedPersonel = None
        govUser = {
            "first_name": request.POST["gov_first_name"],
            "last_name":request.POST["gov_last_name"],
            
        }
        
        try:
            FedPersonel = get_object_or_404(FederationPersonel, user = user)  
        except:
            messages.error("Please add your personal information in order to select your fededertion")
            return redirect("new_personnel")
            
            
        federation = Federation.objects.create(
            user = user,
            FederationPersonel = FedPersonel,
            FederationName = request.POST["FederationName"],
            year = datetime.now().year,
            
        )
        is_sent = AlertGovManager(request, request.POST["govEmail"], govUser,federation)
        print("is_sent: ",is_sent)
        messages.success(request, "Great you have selected your feration, you may continue with your application ")
        if is_sent:
            messages.success(request, 'Please note the we have notified the current "Governance"')
        return redirect("CreateApplication")
    
    
@api_view(["GET", "POST"])
def colorControl(request, federationName):
    if request.method =='GET':
        try:
            federation = get_object_or_404(Federation, FederationName =federationName, is_Gov_approved= "Pending" )
            
            obj = {
                "colors_first_name":federation.FederationPersonel.first_name,
                "colors_last_name":federation.FederationPersonel.last_name,
                "colorsEmail": federation.user.email,
                "colers_Id_number":federation.FederationPersonel.id_number,
                "date_requested": federation.date_requested,
                "federatio_name":federation.FederationName
            }
            return Response({"colors_user": obj})
        except:
            return Response({"colors_user": "Not_found"})
    if request.method =='POST':
        print("Posted status: ", request.POST["Status"]) 
        try:
            
            federation = get_object_or_404(Federation, FederationName =federationName, is_Gov_approved= "Pending" )
            if request.POST["Status"] == 'Approved':
                federation.is_Gov_approved = request.POST["Status"]
                federation.date_approved = datetime.now()
                federation.save()
            elif request.POST["Status"] == 'Declined':
                federation.user.delete()
                pass

            return Response({"request":request.POST["Status"] })
        except:
            return Response({"requst": "Not_found!"})
            
        
           
           
def filterFederations(list):
    
    theList = []
    for item in list:
        print("item name: ",item["federationName"])
        try:
            fed  =get_object_or_404(Federation, FederationName = item["federationName"])
            print("found: ",item)
        except:
            theList.append(item)
            
    return theList
    
    
    
def AlertColorsManager(request, to_email, goveUser, federation, status):
    user = request.user
    is_sent = False
    print(f"To user: {user.username}")
    mail_subject = "Colours application federation representative."
    message = render_to_string("manage_personnel/AlertColorsManager.html",{
        'federationPersonel':federation,
        'user':user,
        'goveUser':goveUser,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http',
        "status":status,
    })
    print(to_email)
    try:
        send_mail(mail_subject,f"{message}"  ,'',[f'{to_email}'], fail_silently=False)
        is_sent = True
    except:
        
        pass     
    
    return is_sent
        
         