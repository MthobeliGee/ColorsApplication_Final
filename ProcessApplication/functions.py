from MyApp.models import *
from django.shortcuts import  get_object_or_404
from LoginManager.tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.models import User



def alert_applicant_state(request, application, applicantApplication):
    
    sportsPerson = applicantApplication.SportsPerson
    mail_subject = "Colors application status update."
    message = render_to_string("ProcessApplication/alerts/alert_applicant_state.html",{
        'sportsPerson':sportsPerson,
        'application':application,
        'applicantApplication':applicantApplication,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    try:
        send_mail(mail_subject,f"{message}"  ,'',[f'{sportsPerson.user.email}'], fail_silently=False)
        return True
    except:
        return False       

def alert_federation_state(request, application, fedUser):
    

    mail_subject = "Colors application status update."
    message = render_to_string("ProcessApplication/alerts/alert_federation_state.html",{
        'fedUser':fedUser,
        'application':application,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    try:
        send_mail(mail_subject,f"{message}"  ,'',[f'{fedUser.email}'], fail_silently=False)
        return True
    except:
        return False 
    
def alert_Kznsc_reviewed(request, application, KznscUser):
    

    mail_subject = "Colors Application Awaiting Awarding."
    message = render_to_string("ProcessApplication/alerts/alert_Kznsc_reviewed.html",{
        'KznscUser':KznscUser,
        'application':application,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    try:
        send_mail(mail_subject,f"{message}"  ,'',[f'{KznscUser.email}'], fail_silently=False)
        return True
    except:
        return False 
    
def toApplicants(request, application):
    applicants = ApplicantApplication.objects.filter(Application = application,status = "OnTeam")
    numApplicantsAlerted  =0
    for applicantApplication in applicants:
        if alert_applicant_state(request, application, applicantApplication):
            numApplicantsAlerted += 1
    return numApplicantsAlerted

def toKZNSC(request, application):
    
    kznscusers = User.objects.filter(is_superuser = True)
    numKZNSC_alerted = 0
    for KznscUser in kznscusers:
        alert_Kznsc_reviewed(request, application, KznscUser)
        numKZNSC_alerted += numKZNSC_alerted
    return numKZNSC_alerted
        
def sendStateAlert(request, application):

    numApplicantsAlerted =  toApplicants(request,application)
    federation_state =  alert_federation_state(request,application, application.user)
    if  numApplicantsAlerted > 0 and federation_state:
        if application.ApplicationStatus == "Approved":
            numKZNSC_alerted =  toKZNSC(request, application)
            if numKZNSC_alerted > 0:
                return True
            else:
                return False
        else:
            return True 
    else:
        return False   
    
    
def alert_declined_Applicant(request, applicantApplicationId):
    
    applicantApplication = get_object_or_404(ApplicantApplication, pk = applicantApplicationId)
    application = applicantApplication.Application
    sportsPerson = applicantApplication.SportsPerson
    
    payload = {
        "application":application,
        "applicantApplication":applicantApplication,
        "sportsPerson":sportsPerson,
        "domain": get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
        
        
    }      
    mail_subject = "Colors Application Awaiting Awarding."
    message = render_to_string("ProcessApplication/alerts/alert_declined_Applicant.html",payload)
    try:
        send_mail(mail_subject,f"{message}"  ,'',[f'{sportsPerson.user.email}'], fail_silently=False)
        return True
    except:
        return False 