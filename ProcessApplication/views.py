from django.shortcuts import render,redirect, get_object_or_404
from MyApp.models import *
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
from .functions import *

def application_List(request):
    
    applications = Application.objects.filter(ApplicationStatus = 'Pending')
    


@login_required
def ApproveApplication(request, applicationId):
    
    try:
        application =  get_object_or_404(Application, pk = applicationId)     
    except:
        messages.error(request, "The applicatrion you tried to modify if not existent for unknown reasons")
        return redirect("home") 
    
    if request.method == 'GET':
        messages.warning(request, "Are you sure you want to 'approve' this application?")
        informationOBJ = {
            "application": application,
        }
        
        return render(request, 'ProcessApplication/ApproveApplication.html', informationOBJ)
    
    
    if request.method == 'POST':
        
        
        application.ApplicationStatus = "Approved"
        application.Step = "Approved"
        application.save()
        sendStateAlert(request,application)
       
        messages.success(request, 'The application for colors has been successfully approved and is now awaiting awarding by the KZNSC')
        
        return redirect("Application_review", applicationId =  application.ApplicationId)
    
    
    
@login_required
def DeclineApplication(request, applicationId):
    
    try:
        
        application = get_object_or_404(Application, pk = applicationId)
        
    except:
        messages.error(request, "The applicatrion you tried to modify if not existent for unknown reasons")
        return redirect("home") 
    
    if request.method == 'GET':
        messages.warning(request, "Are you sure you want to 'decline' this application?")
        informationOBJ = {
            "application": application,
        }
        
        return render(request, 'ProcessApplication/DeclineApplication.html', informationOBJ)
    
    
    if request.method == 'POST':
        
        
        application.ApplicationStatus = "Declined"
        application.Step = "Declined"
        application.isHistory = True
        application.DeclineReason = request.POST["DeclineReason"]
        
        application.save()
        sent = alert_Declined_Application(request, application.user.email,application,application.user)
        
        if sent == False:
            messages.warning(request, "Something went wrong while trying to alert the applicant abount the result of the application please use detials below to communicate manually")
        messages.success(request, 'Application for colors has been declined successfully')
        
        return redirect("Application_review", applicationId =  application.ApplicationId)
    
    
def declineApplicant_committee(request, applicantApplicationId):
    applicantApplication = get_object_or_404(ApplicantApplication, pk = applicantApplicationId)
    application = applicantApplication.Application
    sportsPerson = applicantApplication.SportsPerson
    
    if request.method == 'GET':
        
        payload = {
            "applicantApplication": applicantApplication,
            "application":application,
            "sportsPerson":sportsPerson,
        }
        messages.warning(request, "Are you sure you want to 'decline' this applicant?")
        return render(request, 'ProcessApplication/declineApplicant.html', payload)
    elif request.method =='POST':
        applicantApplication.declineReason = request.POST["declineReason"]
        applicantApplication.status = "Declined"
        applicantApplication.is_deleted = True
        applicantApplication.save()
        alert_declined_Applicant(request,applicantApplication.ApplicantApplicationId)
        messages.success(request, "The applicant has been removed from the team.")
        return redirect("Applcants", applicationId = application.ApplicationId)
        
        
     
def alert_Approved_Application(request, to_email, application, Applicant_user):
    is_sent = False
    mail_subject = "Application result."
    message = render_to_string("ProcessApplication/alert_Approved_Application.html",{
        'Applicant_user':Applicant_user,
        'application':application,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    print(to_email)
    if to_email:
        try:
            send_mail(mail_subject,f"{message}"  ,'',[to_email], fail_silently=False)
            is_sent = True
        except:
            pass
    
    return is_sent

def alert_Declined_Application(request, to_email, application, Applicant_user):
    
    is_sent = False
    mail_subject = "Application result."
    message = render_to_string("ProcessApplication/alert_Declined_Application.html",{
        'Applicant_user':Applicant_user,
        'application':application,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    print(to_email)
    if to_email:
        try:
            send_mail(mail_subject,f"{message}"  ,'',[to_email], fail_silently=False)
            is_sent = True
        except:
            pass
    
    return is_sent


@login_required
def CancelApplication(request, applicationId):
    
    try:
        application = get_object_or_404(Application, pk = applicationId)
    except:
        messages.error(request, "The application you tried to access could not found")
        return redirect("home")    
    
    
    
    if request.method == 'GET':
        
        informationOBJ=  {
            "application":application
        }
        return render(request, 'ProcessApplication/CancelApplication.html',informationOBJ)
    
    
    if request.method == 'POST':
        
        
        try:
            application = get_object_or_404(Application, pk = int(request.POST["applicationId"]))
            
        except:
            
            messages.error(request, "The application you tried to access could not be found")
            return redirect("home")
        
        
        application.ApplicationStatus = "Canceled"
        application.CancelReason = request.POST["CancelReason"]
        application.isHistory = True
      
        application.Step =  "Canceled"
        
        application.save()
  
        messages.success(request, 'Application has been canceled successfully')
        
        adminUsers = User.objects.filter(is_superuser = True)
        numSent = 0
        
        for admin in adminUsers:
            
            if alert_admin_cancel(request,admin.email,application,admin ):
                numSent += 1
                
        if numSent > 0:
            messages.success(request, "Admin alerted")
        
        return redirect("Application_review", applicationId=application.ApplicationId)
        
        
    
def alert_admin_cancel(request, to_email, application, admin_user):
    is_sent = False
    mail_subject = "Colors application canceled."
    message = render_to_string("ProcessApplication/alert_admin_cancel.html",{
        'admin_user':admin_user,
        'application':application,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    print(to_email)
    if to_email:
        try:
            send_mail(mail_subject,f"{message}"  ,'',[to_email], fail_silently=False)
            is_sent = True
        except:
            pass
    
    return is_sent  


@login_required
def addApparel(request, applicationId):
    
    application = None
    
    try:
        application = get_object_or_404(Application, pk = applicationId)
    except:
        messages.error(request, "The application you tried to access is not found")
        return redirect("home")
    
    
    if request.method =='GET':
        
        return render(request, 'ProcessApplication/addApparel.html', {"application":application})
    #now I am currently adding the view for this function
    
    
    if request.method =='POST':
        user  = request.user
        # currenty doinng the part where the super user will ad the letter to approve clothing staff
        #next we will go to the Gov.com application to make approval for the fedration acces for this
        apparel = Apparel.objects.create(
            user = user,
            application = application,
            letter = request.POST["letter"]
        )
        application.ApplicationStatus = "Active"
        application.Step = "Active"
        application.save()
        messages.success(request, 'The letter for apparel has been uploaded suceessfully')
        return redirect("Application_review", applicationId= application.ApplicationId)
        

@login_required
def noLetterActivate(request, applicationId):
    
    application = None
    
    try:
        application = get_object_or_404(Application, pk = applicationId)
        
    except:
        messages.error(request, "The application you tried to access was not found")
        return redirect("home")
    
    
    if request.method == 'POST':
        user = request.user
        application.ApplicationStatus = "Active"
        application.save()
        
        messages.success(request, "The application has been marked as \"Active\".")
        return redirect("Application_review", applicationId=application.ApplicationId)
    
@login_required    
def approveApplicant(request):
    user = request.user
    try:
        applicantApplication = get_object_or_404(ApplicantApplication, pk= request.POST["applicantApplicationId"])
        if user != applicantApplication.Application.user:
            if user.is_staff == False:
                if user.is_superuser == False:
                    messages.error(request, "You are not authorized to access the record")
                    return redirect("home")   
    except:
        messages.error(request, "The rerord you tried to access was not found.")
        return redirect("home")
    
    applicantApplication.status = "OnTeam"
    applicantApplication.save()
    alert_applicant_onTeam(request,applicantApplication.ApplicantApplicationId)
    messages.success(request, "The applicant has been approved to team successfully.")
    return redirect("ApplicantInfo", applicantApplicationId = applicantApplication.ApplicantApplicationId)
    
    
        
@login_required    
def declineApplicant(request):
    user = request.user
    try:
        applicantApplication = get_object_or_404(ApplicantApplication, pk= request.POST["applicantApplicationId"])
        if user != applicantApplication.Application.user:
            if user.is_staff == False:
                if user.is_superuser == False:
                    messages.error(request, "You are not authorized to access the record")
                    return redirect("home")   
    except:
        messages.error(request, "The rerord you tried to access was not found.")
        return redirect("home")
    
    applicantApplication.status = "Declined"
    applicantApplication.save()
    alert_applicant_onTeam(request,applicantApplication.ApplicantApplicationId )
    messages.success(request, "The applicant has been declined successfully.")
    return redirect("ApplicantInfo", applicantApplicationId = applicantApplication.ApplicantApplicationId)
    
    
    
def alert_applicant_onTeam(request,applicantApplicationId):
    applicantApplication = get_object_or_404(ApplicantApplication, pk = applicantApplicationId)
    sportsPerson = applicantApplication.SportsPerson
    application =applicantApplication.Application
    is_sent = False
    
    mail_subject = ""
    message = render_to_string("ProcessApplication/alerts/alert_applicant_onTeam.html",{
        
        'applicant':sportsPerson,
        'ColorsApplication':application,
        'applicantApplication':applicantApplication,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    try:
        send_mail(mail_subject,f"{message}"  ,'',[sportsPerson.Email], fail_silently=False)
        is_sent = True
    except:
        pass
    return is_sent