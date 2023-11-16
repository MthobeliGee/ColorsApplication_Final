from django.shortcuts import render,redirect, get_object_or_404
from MyApp.models import Application,Represantative, CommitteeMember, TeamOfficial,Thefunctions
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

def application_List(request):
    
    applications = Application.objects.filter(ApplicationStatus = 'Pending')
    


@login_required
def ApproveApplication(request, applicationId):
    
    try:
        
        application = get_object_or_404(Application, pk = applicationId)
        
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
        sent = alert_Approved_Application(request, application.user.email,application,application.user)
        
        if sent == False:
            messages.warning(request, "Something went wrong while trying to alert the applicant abount the result of the application please use detials below to communicate manually")
        messages.success(request, 'Application for colors has been approved successfully')
        
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


