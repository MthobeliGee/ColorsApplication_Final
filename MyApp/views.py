from django.shortcuts import render,redirect, get_object_or_404
from .models import *
from manage_personnel.models import *
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
from .functions import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse



def testTemp(request):
    
    
    return render(request, 'MyApp/test.html')


def Home(request):
    application  = None
    
    if request.user.is_authenticated:
       
        try:
            application = get_object_or_404(Application, user = request.user, ApplicationStatus='Oncreate')
        except:
                try:
                    application = get_object_or_404(Application, user = request.user, ApplicationStatus='Complete')
                except:
                    try:
                        application = get_object_or_404(Application, user = request.user, ApplicationStatus='Pending')
                    except:
                        pass
                    pass
            
            
        #Gov app code
        Pendingcolors = None
        # try:
        # user = request.user
        # fedP = get_object_or_404(FederationPersonel, user = request.user)
        # url = 'http://127.0.0.1:8000/pendingFedPersonel/'+ fedP.FederationName+'/'
    
        # r = requests.get(url)
        # print(r.status_code)
    
        # Pendingcolors = r.json()
        # print(Pendingcolors)
        # except:
        #     pass
       
    return render(request,'MyApp/Home.html', {"application":application})



@login_required
def CreateApplication(request):
    user = request.user
    
    federationPersonel = None
    federation = None

    try:
        federationPersonel = get_object_or_404(FederationPersonel, user = user)
        try:
            federation = get_object_or_404(Federation, FederationPersonel =federationPersonel, year = datetime.now().year )   
        except:
            messages.error(request, "Please Select your federation")
            return redirect("getFederation")
    except:
        messages.error(request, "Please add your personal information.")
        return redirect("new_personnel")
    
    if request.method == 'GET':
        
        try:
            application = get_object_or_404(Application, user = user, ApplicationStatus = "Complete")
            if application:
                messages.warning(request, "You have one application that is not yet submitted, please review details below")
                return redirect("Application_review", applicationId = application.ApplicationId)
            
        except:
            try:
                application = get_object_or_404(Application, user = user, ApplicationStatus = "Oncreate")
                if application:
                    messages.warning(request, "You have one application that is not yet submitted, please scroll to move to complete the next step.")
                    return redirect("home")
                
            except:
                pass
            
   
        
        return render(request, 'MyApp/CreateApp.html', {"federationPersonel":federationPersonel, "federation":federation})
    
    if request.method == 'POST':
       
        application = Application.objects.create(
                user = user,
                Federation = federation,
                EventName = request.POST['EventName'],
                StartDate = request.POST['StartDate'],
                EndDate = request.POST['EndDate'],
                HostCity = request.POST['HostCity'],
                HostProvince = request.POST['HostProvince'],
                NumberOfTeam = request.POST['NumberOfTeam'],
                MethodOfSelection = request.POST['MethodOfSelection'],
                SelectionApprovedDate = request.POST['SelectionApprovedDate'],
                TravelDateTime = request.POST["TravelDate"]+" "+ request.POST["TravelTime"],
                ModeOfTravel = request.POST['ModeOfTravel'],
        
       )
        application = get_object_or_404(Application, user = user, ApplicationStatus = "Oncreate")
        print("application.StartDate: ", type(application.StartDate))
       
        messages.success(request, 'The information has been saved successfully, proceed to upload documents.') 
                
                
                
        return redirect("Upload_Documents", applicationId= application.ApplicationId)
@login_required
def addTeamOfficial(request, applicationId):
    application = get_object_or_404(Application, pk = applicationId)
    if request.method == 'GET':
        teamOfficials = TeamOfficial.objects.filter(application = application)
        print(teamOfficials)
        
        return render(request, 'MyApp/addTeamOfficial.html', {"teamOfficials":teamOfficials, "application":application})
    
    
    if request.method == 'POST':
        isIdSubmit = False
        isAceptencSubmited = False
      
        
        if request.POST["AcceptanceofTeamAppointment"] == 'yes':
            isAceptencSubmited = True
            
        if request.POST["IDCopySubmited"] == 'yes':
            
            isIdSubmit = True
        
        officials = TeamOfficial.objects.filter(application = application)
        if Thefunctions.getObjectCount(officials) == 0:
            application.Step = 'addTeamOfficial'
            application.save()
        teamOfficial = TeamOfficial.objects.create(
            application = application,
            FirstName = request.POST["FirstName"],
            LastName = request.POST["LastName"],
            Gender = request.POST["Gender"],
            Designation = request.POST["Designation"],
            IDCopySubmited = isIdSubmit,
            AcceptanceofTeamAppointment = isAceptencSubmited
            
        )
        
        messages.success(request, "Official information saved successfully.")
        return redirect("addTeamOfficial", applicationId =application.ApplicationId)
        
        
    
    
    
    if request.method =='POST':
        
        teamOfficial = TeamOfficial.objects.create(
            application = application,
            FirstName = request.POST["FirstName"],
            LastName  = request.POST["LastName"],
            Gender =  request["Gender"],
            Designation = request.POST["Designation"],
            #IDCopySubmited
            #AcceptanceofTeamAppointment
        )
        
        messages.success(request,"Official add successfully, you may proceed to add more.")
        
        return redirect("addTeamOfficial",applicationId = teamOfficial.application.ApplicationId)
    
    
@login_required
def event_fderations(request):
    
    applications = Application.objects.filter(is_App_taking=True)
    
    
    
@login_required  
def update_team_official(request, officialId):
    
    teamOfficial = get_object_or_404(TeamOfficial, pk = officialId)
    application = teamOfficial.application
    
    if request.method == 'GET':
        
        return render(request, 'MyApp/update_team_official.html', {"teamOfficial":teamOfficial, "application":application})
    
    if request.method == 'POST':
        
        numUpdates = 0
        isIdSubmit = False
        isAceptencSubmited = False
        print(request.POST["Gender"])
        if request.POST["AcceptanceofTeamAppointment"] != 'none':
            if request.POST["AcceptanceofTeamAppointment"] == 'yes':
                isAceptencSubmited = True
        if request.POST["IDCopySubmited"] != 'none':
            
            if request.POST["IDCopySubmited"] == 'yes':
                isIdSubmit = True
        
        if request.POST["FirstName"] != teamOfficial.FirstName:
            
            teamOfficial.FirstName = request.POST["FirstName"]
            numUpdates += 1
            print("FirstName")
            
        if request.POST["LastName"] !=  teamOfficial.LastName:
            
            teamOfficial.LastName = request.POST["LastName"]
            numUpdates += 1
            print("LastName")
            
        if request.POST["Gender"] != teamOfficial.Gender and request.POST["Gender"] != 'none':
            
            teamOfficial.Gender = request.POST["Gender"]
            numUpdates += 1
            print("Gender")
            
        if request.POST["Designation"] != teamOfficial.Designation:
            
            teamOfficial.Designation = request.POST["Designation"]
            numUpdates += 1
            print("Designation")
            
        if teamOfficial.IDCopySubmited != isIdSubmit:
            teamOfficial.IDCopySubmited = isIdSubmit
            numUpdates += 1
            print("IDCopySubmited")
            
            
        if teamOfficial.AcceptanceofTeamAppointment != isAceptencSubmited:
            teamOfficial.AcceptanceofTeamAppointment = isAceptencSubmited
            numUpdates += 1
            print("AcceptanceofTeamAppointment")
            
        if numUpdates >0:
            teamOfficial.save()
            messages.success(request, "Changes saved successfully")
        else:
            messages.info(request, "No changes made on the record.")
            
        return redirect("addTeamOfficial",applicationId = teamOfficial.application.ApplicationId)
        
@login_required
def remove_team_official(request, officialId):
    
    teamOfficial = get_object_or_404(TeamOfficial, pk = officialId)
    application = teamOfficial.application
    
    if request.method =='GET':
        
        messages.warning(request, "Are you sure you want to remove this record?")
        
        return render(request,'MyApp/remove_team_official.html', {"application":application, "teamOfficial":teamOfficial} ) 
    
    if request.method =='POST':
        
        teamOfficial.delete()
        messages.success(request, "The record has been removed successfully")
        return redirect("addTeamOfficial",applicationId = application.ApplicationId)   
    
    
    
@login_required   
def ViewDetails(request, ApplicationId):
    
    application = get_object_or_404(Application,pk=ApplicationId)
    print(application)
    
    return render(request, 'MyApp/ViewDetails.html',{"application":application})
@login_required
def UpdateDetails(request, ApplicationId):
    application = get_object_or_404(Application, pk= ApplicationId)
    if request.method =='GET':
        
        return render(request, 'MyApp/UpdateDetails.html', {"application":application})
 

    if request.method =='POST':
        
        numUpdate = 0
        
        if request.POST["EventName"] != application.EventName:
            
            application.EventName =request.POST["EventName"]
            numUpdate += 1
            
        if request.POST["StartDate"] != application.StartDate:
            
            application.StartDate =request.POST["StartDate"]
            numUpdate += 1
            
        if request.POST["EndDate"] != application.EndDate:
            
            application.EndDate =request.POST["EndDate"]
            numUpdate += 1
            
        if request.POST["HostProvince"] != application.HostProvince:
            
            application.HostProvince =request.POST["HostProvince"]
            numUpdate += 1
            
        if request.POST["RepresatativeType"] != application.RepresatativeType:
            
            application.RepresatativeType =request.POST["RepresatativeType"]
            numUpdate += 1
            
        if request.POST["NumberOfTeam"] != application.NumberOfTeam:
            
            application.NumberOfTeam =request.POST["NumberOfTeam"]
            numUpdate += 1
            
        if request.POST["MethodOfSelection"] != application.MethodOfSelection:
            
            application.MethodOfSelection =request.POST["MethodOfSelection"]
            numUpdate += 1
            
        if request.POST["TravelDateTime"] != application.TravelDateTime:
            
            application.TravelDateTime =request.POST["TravelDateTime"]
            numUpdate += 1
            
        if request.POST["ModeOfTravel"] != application.ModeOfTravel:
            
            application.ModeOfTravel =request.POST["ModeOfTravel"]
            numUpdate += 1
            
            
        if numUpdate > 0 :
            application.save()
            messages.success(request, f'{numUpdate} changes made.')
        else:
            messages.success(request, ''+numUpdate +'changes made.')
            
        return redirect("UpdateDetails", ApplicationId = application.ApplicationId)
            
@login_required           
def AddRepp(request, applicationId):
    application = get_object_or_404(Application, pk = applicationId)
    represantatives = Represantative.objects.filter(application = application)
        
    if request.method == 'GET':
        return render(request, 'MyApp/AddRepp.html', {"application":application, "represantatives":represantatives})
        
    if request.method == 'POST':
        isIdSubmit = False
        isAceptencSubmited = False
        is_parent = False 
      
        Repps = Represantative.objects.filter(application = application)
        
        if Thefunctions.getObjectCount(Repps) == 0:
            application.Step = 'AddRepp'
            application.save()
        if request.POST["AcceptanceofTeamAppointment"] == 'yes':
            isAceptencSubmited = True
            
        if request.POST["IDCopySubmited"] == 'yes':
            isIdSubmit = True
            
        if request.POST["is_parent"] == 'yes':
            is_parent = True
            
        Rep = Represantative.objects.create(     
          
           application = application,
           Id_number = request.POST["Id_number"],
            FirstName = request.POST['FirstName'],
            Surname = request.POST['Surname'],
            Gender = request.POST['Gender'],
            PhoneNumber = request.POST['PhoneNumber'],
            Email = request.POST['Email'],
            City = request.POST['City'],
            Province = request.POST["Province"],
            RepresatativeType = request.POST["RepresatativeType"],
            IDCopySubmited = isIdSubmit,
            AcceptanceofTeamAppointment = isAceptencSubmited,
            is_parent = is_parent,
            
        )
       
        
    
        messages.success(request, "Your information has been saved successfully, please accept team and conditions provided by ", application.Federation.FederationName)
        
        return redirect("applicatntTerms",applicantId = Rep.RepresantativeId,applicant_type ="Athlete",applicationId=application.ApplicationId)

            

@login_required
def applicatntTerms(request, applicantId, applicant_type, applicationId):
    application = get_object_or_404(Application, pk = applicationId)
    athlete = None
    official = None
    comittee = None
    if applicant_type == 'Athlete':
        try:
            athlete = get_object_or_404(Represantative, pk = applicantId)
        except:
            messages.error(request, "The record you tried to access was not found")
            return redirect("home")
    elif applicant_type == 'Official':
        try:
            official = get_object_or_404(TeamOfficial, pk = applicantId )
            
        except:
            messages.error(request, "The record you tried to access was not found")
            return redirect("home")
    elif applicant_type == 'Comittee':
        try:
            comittee = get_object_or_404(CommitteeMember, pk = applicantId)
        except:
            messages.error(request, "The record you tried to access was not found")
            return redirect("home")
        
    applicantTeams = ApplicantTeams.objects.filter( Federation =application.Federation )
    if request.method == 'GET':
        obj = {
            "application":application,
            "athlete":athlete,
            "official":official,
            "comittee":comittee,
            "applicantTeams":applicantTeams
            
            
        }
            
        return render(request, 'MyApp/applicatntTerms.html',obj)      
    elif request.method == 'POST':
        is_saved = False
        if applicant_type == 'Athlete':
            try:
                athlete.is_terms_accepted = True
                athlete.save()
                is_saved = True
            except:
               pass
        elif applicant_type == 'Official':
            try:
                official.is_terms_accepted = True
                athlete.save()
                is_saved = True
            except:
               pass
        elif applicant_type == 'Comittee':
            try:
                comittee.is_terms_accepted = True
                athlete.save()
                is_saved = True
            except:
                messages.error(request, "The record you tried to access was not found")
                return redirect("home")          
        if is_saved:
            
            messages.success(request, "Terms and conditions accepted, please review application and submit.")
        return redirect("ApplicantInfo",  applicantId, applicant_type)
   
@login_required
def ApplicantInfo(request, applicantId, applicant_type):
    application = None
    athlete = None
    official = None
    comittee = None
    instance = None
    if applicant_type == 'Athlete':
        try:
            athlete = get_object_or_404(Represantative, pk = applicantId)
            application = athlete.application
            instance = athlete
        except:
            messages.error(request, "The record you tried to access was not found")
            return redirect("home")
    elif applicant_type == 'Official':
        try:
            official = get_object_or_404(TeamOfficial, pk = applicantId )
            application = official.application
            instance = official
        except:
            messages.error(request, "The record you tried to access was not found")
            return redirect("home")
    elif applicant_type == 'Comittee':
        try:
            comittee = get_object_or_404(CommitteeMember, pk = applicantId)
            application = comittee.application
            instance = comittee
            
        except:
            messages.error(request, "The record you tried to access was not found")
            return redirect("home")
        
    if request.method == 'GET':
        obj = {
            "application":application,
            "athlete":athlete,
            "official":official,
            "comittee":comittee,  
        }
        return render(request, 'MyApp/RepDetails.html', obj)
    elif request.method == 'POST':
        
        instance.status = "Pending"
        instance.user = request.user
        instance.save()
        messages.success(request, "Application for colors has been submitted successfully and is pending approval by manager.")
        #Alert colors federation manageer
        is_alert = alertFedColorsManager(request,applicant_type, instance)
        
        if is_alert == False:
            msg = "Something went wrong while alerting the federation colors manager\n"
            msg += "Please contact the manager at: "+application.Federation.FederationPersonel.user.email+" | "+application.Federation.FederationPersonel.Phone
            messages.warning(request, msg)
        else:
            msg = "The federation manager has been notified of the application."
            messages.success(request, msg)
            
        return redirect("ApplicantInfo", applicantId = applicantId, applicant_type = applicant_type)
            
        
        
        
@login_required
def cancel_applicant_app(request, applicantId, applicant_type ):
   
    if applicant_type == "Athlete":
       instance = get_object_or_404(Represantative, pk = applicantId)
    if applicant_type == "Official" :  
       instance = get_object_or_404(TeamOfficial, pk = applicantId)
    if applicant_type == "Comittee" :  
       instance = get_object_or_404(CommitteeMember, pk = applicantId)
       
    

    is_alert = False
    if   instance.status  == "Pending":
        is_alert = True
    instance.status = "Canceled"
    instance.save()
    
    messages.success(request, 'Your  application has been cancelled successfully')
    if is_alert:
        pass#alert colors fed admin
    
    return redirect("ApplicantInfo", applicantId =applicantId, applicant_type =applicant_type)
    
        
def alertFedColorsManager(request, appType, instance):
    is_sent = False
    application = instance.application
    to_email = application.user.email
    first_name = None 
    
    colors_user =get_colors_user(application)
    mail_subject = "Pending Colors application."
    message = render_to_string("MyApp/alerts/applicantManager_alert.html",{
        "colors_user":colors_user,
        'applicant':get_applicant_user(appType,instance),
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


def get_colors_user(application):
    
    return {
        "first_name":application.user.first_name,
        "last_name":application.user.last_name,
        
    }
    
    


def get_applicant_user(type, instance):
    
    applicant_user = {}
    
    if type == "Athlete":
        applicant_user = {
            "first_name":instance.FirstName,
            "last_name":instance.Surname,
            "email":instance.Email,
            "Phone":instance.PhoneNumber
            
        }
    elif type == "Official":
        applicant_user = {
            "first_name":instance.FirstName,
            "last_name":instance.LastName,
            "email":instance.user.email,
            "Phone":instance.PhoneNumber
            
        }
    elif type == "Comittee":
        applicant_user = {
            "first_name":instance.FirstName,
            "last_name":instance.LastName,
            "email":instance.user.email,
            "Phone":instance.PhoneNumber
            
        }
        
    return applicant_user
    
    
      
@login_required
def update_Representative(request, represantativeId):
    
    represantative = get_object_or_404(Represantative, pk = represantativeId)
    application = represantative.application
    
    if request.method == 'GET':
        
        return render(request, 'MyApp/update_Representative.html', {"represantative":represantative, "application":application})
    
    if request.method == 'POST':
        
        numUpdates = 0
        isIdSubmit = False
        isAceptencSubmited = False
        print(request.POST["Gender"])
        if request.POST["AcceptanceofTeamAppointment"] != 'none':
            if request.POST["AcceptanceofTeamAppointment"] == 'yes':
                isAceptencSubmited = True
        if request.POST["IDCopySubmited"] != 'none':
            
            if request.POST["IDCopySubmited"] == 'yes':
                isIdSubmit = True
                
        if request.POST["Id_number"] != represantative.Id_number:
            represantative.Id_number = request.POST["Id_number"]
            numUpdates += 1    
        if request.POST["FirstName"] != represantative.FirstName:
            represantative.FirstName = request.POST["FirstName"]
            numUpdates += 1
            
        if request.POST["Surname"] != represantative.Surname:
            
            represantative.Surname = request.POST["Surname"]
            numUpdates += 1
            
        if request.POST["Gender"] != 'none':
            if request.POST["Gender"] != represantative.Gender:
                
                represantative.Gender = request.POST["Gender"]
                numUpdates += 1
                
        if request.POST["PhoneNumber"] != represantative.PhoneNumber:
            represantative.PhoneNumber = request.POST["PhoneNumber"]
            numUpdates += 1
            
        if request.POST["Email"] != represantative.Email:
            represantative.Email = request.POST["Email"]
            numUpdates += 1
            
        if request.POST["City"] != represantative.City:
            represantative.City = request.POST["City"]
            numUpdates += 1
         
        if request.POST["Province"] != represantative.Province:
            represantative.Province = request.POST["Province"]
            numUpdates += 1
            
        if request.POST["RepresatativeType"] != 'none':
            if request.POST["RepresatativeType"] != represantative.RepresatativeType:
                represantative.RepresatativeType = request.POST["RepresatativeType"]
                numUpdates += 1
                
        if represantative.IDCopySubmited != isIdSubmit:
            represantative.IDCopySubmited = isIdSubmit
            numUpdates +=1 
            
        if represantative.AcceptanceofTeamAppointment != isAceptencSubmited:
            
            represantative.AcceptanceofTeamAppointment = isAceptencSubmited
            numUpdates +=1 
            
        if numUpdates > 0:
            
            represantative.save()
            messages.success(request, "Changes saved successfully")
        else:
            messages.info(request, "There were no changes made on the record.")
        return redirect("ApplicantInfo",applicantId=represantative.RepresantativeId, applicant_type = "Athlete")
            

@login_required
def remove_Representative(request, represantativeId):
    
    represantative = get_object_or_404(Represantative, pk = represantativeId)
    application = represantative.application
    if request.method =='GET':
        messages.warning(request, "Are you sure you want to remove the record?")
        return render(request, 'MyApp/remove_Representative.html', {"represantative":represantative, "application":application})
    
    if request.method == 'POST':
        
        represantative.delete()
        messages.success(request, "The record is deleted successfully.")
        
        return redirect("AddRepp", applicationId = application.ApplicationId)
        
@login_required
def RepDetails(request, RepresantativeId):
    
    Rep =get_object_or_404(Represantative, pk= RepresantativeId)
    print(Rep)
    
    return render (request, 'MyApp/RepDetails.html',{"Rep":Rep}) 
@login_required
def Add_Committee_Member(request):

    #CommitteeMemberDetails(request, ):'
    try:
        member = get_object_or_404(CommitteeMember, is_history = False)
        if member:
            messages.info(request, "You already have an active committee profile, see details below")
            return redirect("CommitteeMemberDetails", MemberId = member.CommitteeMemberId)
    except:
        pass
        
    if request.method == 'GET':
        
        return render(request, 'MyApp/Add_Committee_Member.html')
    
    if request.method == 'POST':
        
        
        committeeMember = CommitteeMember.objects.create(
            
            user = request.user,
            Id_number = request.POST["id_number"],
            FirstName = request.POST['FirstName'],
            Surname = request.POST['Surname'],
            Gender = request.POST['Gender'],
            Email = request.POST["Email"],
            PhoneNumber = request.POST["PhoneNumber"],
            City = request.POST["City"],
            Province = request.POST["Province"]
        )
        messages.success(request, "Your details have been saved successfully please reciew and submit application")
        return redirect("CommitteeMemberDetails",MemberId=committeeMember.CommitteeMemberId)
    
@login_required
def CommitteeMemberDetails(request, MemberId):
    try:
        committeeMember = get_object_or_404(CommitteeMember, pk= MemberId)
    except:
        messages.error(request, "The record you tried to access does not exit, you may add a new committe application below.")
        return redirect("Add_Committee_Member")
    
    if request.method == "GET":
       
    
        return render(request, 'MyApp/CommitteeMemberDetails.html', {"committeeMember":committeeMember})
    elif request.method == 'POST':
        committeeMember = None
        try:
            committeeMember = get_object_or_404(CommitteeMember, pk = int(request.POST["CommitteeMemberId"]))
        except:
            messages.error(request, "The record you tried to access does not exit")
            return redirect("home")
        
        committeeMember.status = "Pending"
        committeeMember.RequestDate = datetime.now()
        committeeMember.save()
        messages.success(request, "You application for committee membership has been submitted successfully.")
        #alert federation admins
        
        is_alert = new_committee_alert(request,committeeMember)
        if is_alert:
            messages.success(request, "The KZNSC executives have been notified of your application")
        else:
            messages.error(request, "We could not reach any of our KZNSC colors executives please contact them manually, find information on the contact page.")
            
        return redirect("CommitteeMemberDetails", MemberId= MemberId)
        
        
@login_required
def cancel_committee_app(request, memberId):
    member = None
    try:
        
        member = get_object_or_404(CommitteeMember, pk = memberId)
    except:
        
        messages.error(request, "The record you tried to access was not found")
        return redirect("home")
    
    if request.method == 'GET':
        
        return render(request,'MyApp/cancel_committee_app.html',  {"committeeMember":member}) 
    elif request.method == 'POST':
        
        member.is_history = True
        
        
        if request.POST["is_super"] == 'yes':
            member.is_deleted = True
            member.status = "Removed"
            member.ResponseDate = datetime.now()
            remove_committee_alert(request,member)
            messages.success(request, "Member has been removed successfully.")
            
        else:
            member.status = "Canceled"
            messages.success(request, "The application has been canceled successfully.")
            cancel_committee_alert(request,member)
            
            
            
        member.save()    
        
        #alert admins
        return redirect("CommitteeMemberDetails",MemberId=memberId)
    
def remove_committee_alert(request,member):
    is_sent = False
    mail_subject = "KZNSC Colors Committee."
    to_email =member.user.email 
    message = render_to_string("MyApp/alerts/remove_committee_alert.html",{
        'admin_user':request.user,
        'member':member,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    
    if to_email:
        try:
            send_mail(mail_subject,f"{message}"  ,'',[to_email], fail_silently=False)
            is_sent =  True
        except:
            pass
    return is_sent

def cancel_committee_alert(request,committeeMember):
    
    is_sent = False
    num_alert = 0
    mail_subject = "Canceled Colors Committee Application."
    admin_users = User.objects.filter(is_superuser = True)
    for admin_user in admin_users:
        to_email =admin_user.email 
        message = render_to_string("MyApp/alerts/cancel_committee_alert.html",{
            'admin_user':admin_user,
            'committeeMember':committeeMember,
            'domain': get_current_site(request).domain,
            "protocol": 'https' if request.is_secure() else 'http'
        })
        
        if to_email:
            try:
                send_mail(mail_subject,f"{message}"  ,'',[to_email], fail_silently=False)
                num_alert += 1
            except:
                pass
    if num_alert > 0:
           is_sent = True
    return is_sent
         
       
     
def new_committee_alert(request,committeeMember):
    
    is_sent = False
    num_alert = 0
    mail_subject = "Pending Colors Committe Application."
    admin_users = User.objects.filter(is_superuser = True)
    for admin_user in admin_users:
        to_email =admin_user.email 
        message = render_to_string("MyApp/alerts/new_committee_alert.html",{
            'admin_user':admin_user,
            'committeeMember':committeeMember,
            'domain': get_current_site(request).domain,
            "protocol": 'https' if request.is_secure() else 'http'
        })
        
        if to_email:
            try:
                send_mail(mail_subject,f"{message}"  ,'',[to_email], fail_silently=False)
                num_alert += 1
            except:
                pass
    if num_alert > 0:
           is_sent = True
    return is_sent
         
   
@login_required
def update_CommiteeMember(request, CommitteeMemberId):
    
    committeeMember = get_object_or_404(CommitteeMember, pk=CommitteeMemberId)
  

    if request.method =='GET':
        
        return render(request, 'MyApp/update_CommiteeMember.html', {"committeeMember":committeeMember})
    
    if request.method =='POST':
        user = request.user
        numUpdates = 0
        numUserChange = 0
        
        if committeeMember.FirstName != request.POST["FirstName"]:
            committeeMember.FirstName = request.POST["FirstName"]
            numUpdates += 1
            user.first_name = request.POST["FirstName"]
            numUserChange +=1
            
            
        if committeeMember.Surname  != request.POST["Surname"]:
            
            committeeMember.Surname = request.POST["Surname"]
            numUpdates += 1
            user.last_name = request.POST["Surname"]
            numUserChange +=1
        
        if request.POST["Gender"] != 'none':
            if committeeMember.Gender != request.POST["Gender"]:
                committeeMember.Gender = request.POST["Gender"]
                numUpdates += 1
                
        if committeeMember.Email != request.POST["Email"]:
            
            committeeMember.Email = request.POST["Email"]
            numUpdates += 1
            user.email = request.POST["Email"]
            user.username = request.POST["Email"]
            numUserChange +=1
            
        if committeeMember.PhoneNumber != request.POST["PhoneNumber"]:
            
            committeeMember.PhoneNumber = request.POST["PhoneNumber"]
            numUpdates += 1
            
        if committeeMember.City != request.POST["City"]:
            
            committeeMember.City = request.POST["City"]
            numUpdates += 1
            
        if committeeMember.Province != request.POST["Province"]:
            
            committeeMember.Province = request.POST["Province"]
            numUpdates += 1
            
        if numUpdates > 0:
            if numUserChange > 0:
                user.save()
            committeeMember.save()
            messages.success(request, "The changes were saved successfully.")
        else:
            messages.info(request, "No changes made on the record.")
            
        
        return redirect("update_CommiteeMember", CommitteeMemberId=CommitteeMemberId)            


    
@login_required
    
def Upload_Documents(request, applicationId):
    
    application = get_object_or_404(Application, pk = applicationId)
    if application.Step != 'Application_review' and application.Step != 'Pending':
        
        application.Step = 'Upload_Documents'
        application.save()
    if request.method == 'GET':
        
        return render(request, 'MyApp/Upload_Documents.html',{"application":application}) 
    
    if request.method == 'POST':
        if application.Step !='Application_review' and  application.Step =='Pending':
            application.RegulationsInterestDeclaration = request.POST["RegulationsInterestDeclaration"]
            application.SelectionCriteriaProtocols = request.POST["SelectionCriteriaProtocols"]
            
            application.GeneralRegulationSelectionProcedure = request.POST["GeneralRegulationSelectionProcedure"]
            application.TeamOfficialDuties = request.POST["TeamOfficialDuties"]
            application.HighPerformancePlan = request.POST["HighPerformancePlan"]
            application.EventInvitation = request.POST["EventInvitation"]
            application.DocumentationOfSelectionSubmitted = request.POST["DocumentationOfSelectionSubmitted"]
            
            application.save()
            
        else:
            numUpdates = 0
            try:
                if request.POST["RegulationsInterestDeclaration"] != '':
                    application.RegulationsInterestDeclaration = request.POST["RegulationsInterestDeclaration"]
                
                    numUpdates += 1
            except:
                pass
            
            try:
                if request.POST["SelectionCriteriaProtocols"] !='':
                    application.SelectionCriteriaProtocols = request.POST["SelectionCriteriaProtocols"]
                    numUpdates += 1
            except:
                pass
            
            try:
                if request.POST["GeneralRegulationSelectionProcedure"] != '':
                    application.GeneralRegulationSelectionProcedure = request.POST["GeneralRegulationSelectionProcedure"]
                    numUpdates += 1
            except:
                pass
            
            try:
                if request.POST["TeamOfficialDuties"] != '':
                    application.TeamOfficialDuties = request.POST["TeamOfficialDuties"]
                    numUpdates += 1
            except:
                pass
            
            try:
                if request.POST["HighPerformancePlan"] != '':
                    application.HighPerformancePlan = request.POST["HighPerformancePlan"]
                    numUpdates += 1
            except:
                pass
                
            try:
                if request.POST["EventInvitation"] != '':
                    application.EventInvitation = request.POST["EventInvitation"]
                    numUpdates += 1
            except:
                pass
            
            try:
                if request.POST["DocumentationOfSelectionSubmitted"] != '':
                    application.DocumentationOfSelectionSubmitted = request.POST["DocumentationOfSelectionSubmitted"]
                    numUpdates += 1
            except:
                pass
            
            if numUpdates > 0:
               
                application.save()
            else:
              pass   
                
            #return redirect("Upload_Documents", applicationId = application.ApplicationId)
             
            
                
                    
        
        messages.success(request, "Documents uploaded successfully, please proceed to accept code of conduct terms.")
        
        return redirect("termsAndConditions", applicationId = application.ApplicationId)
    

@login_required   
def Remove_CommitteeMember(request, memberId):
    
    committeeMember = get_object_or_404(CommitteeMember, pk = memberId)
    application = committeeMember.application
    
    if request.method == 'GET':
        
        messages.warning(request, "Are you sure you want to emove this record?")
        return render(request, 'MyApp/Remove_CommitteeMember.html', {"committeeMember": committeeMember,"application":application})  
    
    
    if request.method == 'POST':
        
        committeeMember.delete()
        messages.success(request, "The member record was removed successfully")
        
        return redirect("Add_Committee_Member", applicationId=application.ApplicationId) 
            
@login_required          
def termsAndConditions(request, applicationId):
    
    application = get_object_or_404(Application,pk =applicationId)
    
    if request.method == 'GET':
        application.Step = 'termsAndConditions'
        application.save()
        return render(request, 'MyApp/termsAndConditions.html', {"application":application})
    
    
    if request.method == 'POST':
        
        IsAccepted = request.POST["IsAccepted"]
        
        if IsAccepted == 'Yes':
            application.CodeOfConductAcceped = True
            application.Step = 'Application_review'
            application.ApplicationStatus = 'Complete'
            messages.success(request, "Code Of Conduct Acceped, please review the application and submit for approval.")
        else:
            
            application.ApplicationStatus = 'Canceled'
            
            messages.info(request, "By not accepting the code of conduct automatically the application is canceled.")
              
        application.save() 
        return redirect("Application_review", applicationId=application.ApplicationId)
        
        
    
@login_required  
def Application_review(request, applicationId):
    application = None
    try:
        application = get_object_or_404(Application, pk=applicationId)
    except:
        messages.error(request, "The colors application you tried to access is not found")
        return redirect("home")
    represantatives = Represantative.objects.filter(application = application)
    CommitteeMembers = CommitteeMember.objects.filter(application = application)
    teamOfficials = TeamOfficial.objects.filter(application= application)
    numApplicants = ObjectsLength(represantatives)
    numOfficials = ObjectsLength(teamOfficials)
    numCommitee = ObjectsLength(CommitteeMembers)
    user = application.user

    fedPerson = get_object_or_404(FederationPersonel, user = user)

    
    print(fedPerson)
    if application.Step == 'Complete':
        application.Step = 'Application_review'
        application.save()
    if request.method == 'GET':
        
        apparel = None
        if application.ApplicationStatus == "Active" or application.ApplicationStatus == "Sattled":
            try:
                apparel = get_object_or_404(Apparel, application= application)
            except:
                pass
        domain = get_current_site(request)
        informationOBJ = {
            "numCommitee":numCommitee,
            "numOfficials":numOfficials,
            "application":application,
            "represantatives":represantatives,
            "CommitteeMembers":CommitteeMembers,
            "teamOfficials":teamOfficials,
            "numApplicants":numApplicants,
            "FederationPersonel":fedPerson, 
            "apparel":apparel,
            "domain":domain
            }
        return render(request, 'MyApp/Application_review.html', informationOBJ)
    
    if request.method == 'POST':
        
        valid = checkDate(str(application.StartDate))
        if valid:
            application.ApplicationStatus = 'Pending'
            application.Step = 'Pending'
        
            application.save()
        else:
            application.delete()
            messages.error(request, "you can only make applications for events 30 prior for submission, the application has been removed")
            return redirect("CreateApplication")
        
        
        #alert admin
        adminUsers = User.objects.filter(is_superuser = True)
        
        for admin in adminUsers:
            
            alert_admin_Application(request,admin.email,application,admin )
            
        messages.success(request, "The application has been submitted for consideration successfully")
        
        return redirect("Application_review", applicationId = applicationId)
        

@login_required
def Officials(request, applicationId):
    
    application = get_object_or_404(Application,pk = applicationId)
    Officials = TeamOfficial.objects.filter(application = application)
    
    if request.method == 'GET':
        
        
        return render(request, 'MyApp/Officials.html', {"application":application, "teamOfficials":Officials})
    
    
def Applcants(request,applicationId):
    application = get_object_or_404(Application,pk = applicationId)
    Applicants = Represantative.objects.filter(application = application)
    
    if request.method == 'GET':
        
        return render(request,'MyApp/Applcants.html', {"application":application,"Applicants": Applicants})
    
def Committee(request, type):
    
    
    commitee = CommitteeMember.objects.all()
    
    
    if request.method =='GET':
        
        
        commiteeObj = {
            "numPending":countObj(CommitteeMember.objects.filter(status ="Pending")),
            "numAppved":countObj(CommitteeMember.objects.filter(status ="Approved")),
            "numHistory":countObj(CommitteeMember.objects.filter(is_history = True)),
            "Pending":CommitteeMember.objects.filter(status ="Pending"),
            "Approved":CommitteeMember.objects.filter(status ="Approved"),
            "history":CommitteeMember.objects.filter(is_history = True),
            "commitee":getCommittee(type),
            "type":type
        }
        
        return render(request, 'MyApp/Committee.html', commiteeObj)
    
    
def getCommittee(type):
    
    committee = []
    if type=="Pending":
        committee =CommitteeMember.objects.filter(status ="Pending")
    elif type=="Approved":
        committee = CommitteeMember.objects.filter(status ="Approved")
    elif type == 'history':
        CommitteeMember.objects.filter(is_history = True)
        
    return committee
        
        
        
@login_required
def committee_response(request, memberId, response):
    if request.user.is_superuser == False:
        messages.error(request, 'The action you are trying to take is for KZNSC high renking officials.')
        return redirect("home")
        
    member = None
    try:
        member = get_object_or_404(CommitteeMember, pk = memberId)
    except:
        messages.error(request, "The record you tried to access was not found.")
        return redirect("home")
    
    if request.method == 'GET':
        
        return render(request, 'MyApp/committee_response.html',{"CommitteeMember":member,"response":response })
    
    if request.method =='POST':
        member.status = request.POST["response"]
        member.save()
        committee_response_alert(request,member,response)
        
        if request.POST["response"] == "Approved":
            memberUser = member.user
            memberUser.is_staff = True
            memberUser.save()
            messages.success(request, "The appication has been approved successfully. Applicant has been notified")
        elif request.POST["response"] == "Declined":
            messages.success(request, "The appication has been declened successfully. Applicant has been notified") 
            
        return redirect("CommitteeMemberDetails", MemberId=member.CommitteeMemberId)
        
        
def committee_response_alert(request, member, response):
    #committee_Approve
    #committee_Decline
    res_teplate = 'committee_'+response+'.html'
    
    is_sent = False
    
    mail_subject = "KZNSC Colors, Committe Application."
    admin_user =request.user
    
    to_email =member.Email 
    message = render_to_string('MyApp/alerts/'+res_teplate,{
        'admin_user':admin_user,
        'member':member,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    
    if to_email:
        try:
            send_mail(mail_subject,f"{message}"  ,'',[to_email], fail_silently=False)
            is_sent = True
        except:
            pass
    
    return is_sent
    
    
    
def Documents(request, applicationId):
    
    
    application = get_object_or_404(Application,pk = applicationId)
    docs = get_object_or_404(FedDocuments, Year = datetime.now().year, FederationPersonel = application.FederationPersonel)
    if request.method == 'GET':
        Domain = get_current_site(request)
        
        return render(request, 'MyApp/Documents.html', {"application":application, "docs":docs, "Domain":Domain})
    
    
# detalis pages 
def teamOfficialDetails(request, teamOfficialId):
    
    teamOfficial = get_object_or_404(TeamOfficial, pk=teamOfficialId)
    
    application = teamOfficial.application
    
    return render(request, 'MyApp/teamOfficialDetails.html', {"teamOfficial":teamOfficial,"application":application})
            
def represantativeDetails(request, represantativeId):
    
    represantative = get_object_or_404(Represantative, pk=represantativeId)
    application = represantative.application
    return render(request, 'MyApp/represantativeDetails.html',{"represantative":represantative,"application":application})
            

def ContinueApplication(request, applicationId):
    #Step refers to the already comleted step
    user = request.user
 
    
    application = get_object_or_404(Application, pk=applicationId)
    print(application.Step)
    if application.Step =='start' or application.Step =='addTeamOfficial':
        
        messages.info(request, "You may continue with adding your team officials or continue to the next step")
        return redirect("addTeamOfficial",applicationId = application.ApplicationId)
        
    elif application.Step =='AddRepp':
        messages.info(request, "You may continue with adding your team represantatives or continue to the next step")
        
        return redirect("AddRepp",applicationId = application.ApplicationId)
   
    elif application.Step == 'Add_Committee_Member':
        
        messages.info(request, "You may continue with adding your team committee members or continue to the next step")
        
        return redirect("Add_Committee_Member",applicationId = application.ApplicationId)
    elif  application.Step == 'Upload_Documents':
        #Upload_Documents
        messages.info(request, "Please upload documents save and continue to the next step")
        
        return redirect("Upload_Documents",applicationId = application.ApplicationId)
    elif application.Step == 'termsAndConditions':
        messages.info(request, "Please proceed to accept the terms and conditions for the application to be considered")
        return redirect("termsAndConditions",applicationId = application.ApplicationId)
    elif application.Step == 'Application_review':
        #Application_review
        messages.info(request, "Please proceed to review the application and submit for consideration")
        return redirect("Application_review",applicationId = application.ApplicationId)
        
def ObjectsLength(list):
    
    numObjects = 0
    
    for item in list:
        numObjects += 1
        
    return numObjects


@login_required
def SubmitApplication(request, applicationId):
    
    application = get_object_or_404(Application, pk = applicationId)
    if request.method == 'POST':
        application.Stap = "Pending"
        application.ApplicationStatus = "Pending"
        application.save()
        
        
        
def alert_admin_Application(request, to_email, application, admin_user):
    is_sent = False
    mail_subject = "Pending colors application."
    message = render_to_string("MyApp/alert_admin_Application.html",{
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
def my_applications(request):
    user = request.user
   
    try:
        
        ActiveApplication = get_object_or_404(Application, user = user, ApplicationStatus = "Pending")
    except:
        try:
            ActiveApplication = get_object_or_404(Application, user = user, ApplicationStatus =    "Approved")
        except:
           
            try:
                ActiveApplication = get_object_or_404(Application, user = user, ApplicationStatus = "Active")
            except:
                
                try:
                    ActiveApplication = get_object_or_404(Application, user = user, ApplicationStatus = "Complete")
                except:    
                    ActiveApplication = None 
                  
    
    historyApplications  = []
    if ActiveApplication:
   
        t = sattleApplication(ActiveApplication.ApplicationId)
       
        if t:
            
           
            messages.info(request, "Your application for colors has been sattled due to the end date being reached.")
    myApplications =  Application.objects.filter(user = user)
    
    for application in myApplications:
        
        if application.ApplicationStatus != "Pending"  or application.ApplicationStatus != "Approved":
            
            if application.isHistory:
                historyApplications.append(application)
            
         
    numApplicants = Represantative.objects.filter(application = ActiveApplication).count()
    numOfficials = TeamOfficial.objects.filter(application = ActiveApplication).count()
    numCommitee = CommitteeMember.objects.filter(application = ActiveApplication).count()
    infrmationOBJ = {
        "ActiveApplication":ActiveApplication,
        "numOfficials":numOfficials,
        "numApplicants":numApplicants,
        "numCommitee": numCommitee,
        "historyApplications":historyApplications,
        
    }   
    return render(request, "MyApp/my_applications.html", infrmationOBJ)
        


def sattleApplication(applicationId):
    isSattled = False
    application = get_object_or_404(Application, pk = applicationId)
    
    year = application.EndDate.year
    month = application.EndDate.month
    day = application.EndDate.day
    
    currentYear = datetime.now().year
    currentMonth = datetime.now().month
    currentDay = datetime.now().day
    
    if year < currentYear:
        print("year less")
        isSattled = settle(application.ApplicationId)
    elif year == currentYear:
        print("year = ")
        if month < currentMonth:
            print("month <")
            isSattled = settle(application.ApplicationId)
        elif month == currentMonth:
            if day < currentDay:
                isSattled = settle(application.ApplicationId)
    
    return isSattled
        
        
    
def settle(applicationId):
    
    application = get_object_or_404(Application, pk = applicationId)
    application.ApplicationStatus = "Sattled"
    application.Step = "Sattled"
    application.isHistory = True
    application.save()
    
    return True
    
    

@login_required
def Applications(request):
    
    
    pending = Application.objects.filter(ApplicationStatus = "Pending")
    numApproved =  countObj(Application.objects.filter(ApplicationStatus = "Approved"))
    numActive = countObj(Application.objects.filter(ApplicationStatus = "Active"))
    
    #approved = Application.objects.filter(ApplicationStatus = "Approved")
    print()
    print("pending: ", pending)
    
    
    informationOBJ = {
        "applications":pending,
        "status":"pending",
        "numApproved":numApproved,
        "numActive":numActive
       
    }
    
    return render(request, 'MyApp/allApplication.html', informationOBJ)


@login_required
def Approved(request):
    
    numApproved =  countObj(Application.objects.filter(ApplicationStatus = "Approved"))
    numActive = countObj(Application.objects.filter(ApplicationStatus = "Active"))
    
   
    approved = Application.objects.filter(ApplicationStatus = "Approved")
    print()
    print("approved: ", approved)
    
    
    informationOBJ = {
        "applications":approved,
        "status":"approved",
        "numApproved":numApproved,
        "numActive":numActive
        
       
    }
    
    return render(request, 'MyApp/allApplication.html', informationOBJ)


@login_required
def History(request):
    
    
    
    history = Application.objects.filter(isHistory = True)
    numApproved =  countObj(Application.objects.filter(ApplicationStatus = "Approved"))
    numActive = countObj(Application.objects.filter(ApplicationStatus = "Active"))

    
    
    
    informationOBJ = {
        "applications":history,
        "status":"history",
        "numApproved":numApproved,
        "numActive":numActive
        
        
    }
    
    return render(request, 'MyApp/allApplication.html', informationOBJ)



@login_required
def Active(request):
    
    
    
    Active = Application.objects.filter(ApplicationStatus = "Active")
    numApproved =  countObj(Application.objects.filter(ApplicationStatus = "Approved"))
    numActive = countObj(Application.objects.filter(ApplicationStatus = "Active"))

    
    
    
    informationOBJ = {
        "applications":Active,
        "status":"Active",
        "numApproved":numApproved,
        "numActive": numActive
        
        
    }
    
    return render(request, 'MyApp/allApplication.html', informationOBJ)




def countObj(list):
    
    numItem = 0
    for item in list:
        numItem += 1
        
    return numItem  

@login_required 
def chooseFederation(request):
    federations =[]
    try:
   
       # url = 'https://yonelahopewell1.pythonanywhere.com/GovApisComplayingFederations'
        url = 'https://kznsannualreport.pythonanywhere.com/GovApisComplayingFederations'
        r = requests.get(url)
    
     
        data = r.json()
        
        print()
        federations = data["federations"]
        #print("The request data fed list: ", data["federations"][0]["federationName"])
    except :
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
                    
                }
            ]
        
        pass
    
    if request.method =='GET':
        
        return render(request, 'MyApp/federations.html', {"federations": federations})
    
    
    if request.method == 'POST':
        
        user=  request.user
        try:
            FedPersonel = get_object_or_404(FederationPersonel, user = user)
            FedPersonel.FederationName = request.POST["FederationName"]
            FedPersonel.dateSelected = datetime.now()
            FedPersonel.save()
        except:
            FedPersonel = FederationPersonel.objects.create(
                user = user,
                FederationName = request.POST["FederationName"],
                dateSelected = datetime.now()
            )
            
        AlertGovManager(
            request,
            user,
            request.POST["govEmail"],
            {"first_name": request.POST["gov_first_name"], "last_name":request.POST["gov_last_name"]},
            FedPersonel
        )
        messages.success(request, "Great you have selected your feration, you may continue with your application")
        #alert Governance manager by email
        if FedPersonel.PersonelPhone == None:
            messages.warning(request, "please update your phone number and start again with the application process.")
            return redirect("account")
        return redirect("CreateApplication")
    
    
    

def AlertGovManager(request, to_email, coloresUser, federation):
    user = request.user
    is_sent = False
    print(f"To user: {user.username}")
    mail_subject = "Colours application  representative."
    message = render_to_string("MyApp/AlertGovManager.html",{
        'federationPersonel':federation,
        'user':user,
        'coloresUser':coloresUser,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    print(to_email)
    try:
        send_mail(mail_subject,f"{message}"  ,'',[f'{to_email}'], fail_silently=False)
        is_sent = True
    except:
        
        pass     
    
    return is_sent   

    
    
@api_view(['GET'])
@login_required
def pendingFedPersonel(request, FedName):
    
    
    federationPersonel = None
    application = None
    try:
        federationPersonel = get_object_or_404(FederationPersonel, FederationName=FedName, Status = "Pending")
        application = get_object_or_404(Application, FederationPersonel = federationPersonel)
    except:
        pass
    
    FedPerson = {
        "first_name": federationPersonel.user.first_name,
        "last_name":federationPersonel.user.last_name,
        "email": federationPersonel.user.email,
        "appStatus":application.ApplicationStatus,
        "AppCreateDate":application.DateCreated
        
    }
    
    return JsonResponse(FedPerson)



@api_view(['GET'])
@login_required
def ApproveFedPersonel(request, FedName):
    federationPersonel = None
    try:
        federationPersonel = get_object_or_404(FederationPersonel, FederationName=FedName, Status = "Pending") 
    except:
        pass
    if federationPersonel:
        federationPersonel.Status = "Approved"
        federationPersonel.save()   
    return JsonResponse({"Status":"Approved"})


@api_view(['GET'])
@login_required
def DeclineFedPersonel(request, FedName):
    federationPersonel = None
    try:
        federationPersonel = get_object_or_404(FederationPersonel, FederationName=FedName, Status = "Pending") 
        user = federationPersonel.user
        user.delete()
        
        #alert user 
    except:
        pass
   
    return JsonResponse({"Status":"Declined"})





def Upload_DocumentsTest(request, applicationId):
    
    application = get_object_or_404(Application, pk = applicationId)
    docs  = None
    
    try:
        docs = get_object_or_404(FedDocuments, FederationPersonel = application.FederationPersonel, Year = str(datetime.now().year))
        
    except:
        pass
    if application.Step != 'Application_review' and application.Step != 'Pending':
        
        application.Step = 'Upload_Documents'
        application.save()
    if request.method == 'GET':
        Domain = get_current_site(request)
        return render(request, 'MyApp/Upload_DocumentsTest.html',{"application":application, "docs":docs, "Domain":Domain}) 
    
    if request.method == 'POST':
       
            
            
        if docs == None:
            
            docs = FedDocuments.objects.create(
                FederationPersonel = application.FederationPersonel,
                RegulationsInterestDeclaration = request.FILES["RegulationsInterestDeclaration"],
                SelectionCriteriaProtocols = request.FILES["SelectionCriteriaProtocols"],
                GeneralRegulationSelectionProcedure = request.FILES["GeneralRegulationSelectionProcedure"],
                TeamOfficialDuties = request.FILES["TeamOfficialDuties"],
                HighPerformancePlan = request.FILES["HighPerformancePlan"],
                EventInvitation = request.FILES["EventInvitation"],
                DocumentationOfSelectionSubmitted = request.FILES["DocumentationOfSelectionSubmitted"],
                
                Year = str(datetime.now().year)
            )

        else:
            numUpdates = 0
            try:
                if request.POST["RegulationsInterestDeclaration"] != '':
                    docs.RegulationsInterestDeclaration = request.FILES["RegulationsInterestDeclaration"]
                
                    numUpdates += 1
            except:
                pass
            
            try:
                if request.POST["SelectionCriteriaProtocols"] !='':
                    docs.SelectionCriteriaProtocols = request.FILES["SelectionCriteriaProtocols"]
                    numUpdates += 1
            except:
                pass
            
            try:
                if request.POST["GeneralRegulationSelectionProcedure"] != '':
                    docs.GeneralRegulationSelectionProcedure = request.FILES["GeneralRegulationSelectionProcedure"]
                    numUpdates += 1
            except:
                pass
            
            try:
                if request.POST["TeamOfficialDuties"] != '':
                    docs.TeamOfficialDuties = request.FILES["TeamOfficialDuties"]
                    numUpdates += 1
            except:
                pass
            
            try:
                if request.POST["HighPerformancePlan"] != '':
                    docs.HighPerformancePlan = request.FILES["HighPerformancePlan"]
                    numUpdates += 1
            except:
                pass
                
            try:
                if request.POST["EventInvitation"] != '':
                    docs.EventInvitation = request.FILES["EventInvitation"]
                    numUpdates += 1
            except:
                pass
            
            try:
                if request.POST["DocumentationOfSelectionSubmitted"] != '':
                    docs.DocumentationOfSelectionSubmitted = request.FILES["DocumentationOfSelectionSubmitted"]
                    numUpdates += 1
            except:
                pass
            
            if numUpdates > 0:
                messages.success(request, "Changes saved successfully ")
                docs.save()
            else:
                messages.error(request, 'No changes made')   
                
            return redirect("Upload_Documents", applicationId = application.ApplicationId)
            
            
                    
                        
        
        messages.success(request, "Documents uploaded successfully, please proceed to accept code of conduct terms.")
        
        return redirect("termsAndConditions", applicationId = application.ApplicationId)
    



# def chooseFederation():
#     federations =[]
#     try:
   
#        # url = 'https://yonelahopewell1.pythonanywhere.com/GovApisComplayingFederations'
#         url = 'https://kznsannualreport.pythonanywhere.com/GovApisComplayingFederations'
#         r = requests.get(url)
    
     
#         data = r.json()
        
#         print()
#         federations = data["federations"]
#         #print("The request data fed list: ", data["federations"][0]["federationName"])
#     except :
#         federations =[
#                 {
#                     "federationName":"KZN AQUATICS",
#                     "userName":"Yonela",
#                     "userSurname":"Sitshaka",
#                     "userEmail":"livesoundsmusic@gmail.com"
                    
#                 },
#                 {
#                     "federationName":"SAFA",
#                     "userName":"Hopewell",
#                     "userSurname":"Sitshaka",
#                     "userEmail":"yonela@kznsc.com"
                    
#                 }
#             ]
        
#         pass
    
    
        
#         return federations
    
  
    
    


def newFed(request):
    
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
    
    if request.method == 'GET':

        return render(request,  'MyApp/federations.html',{"federations":federations})
    
    if request.method == 'POST':
        
        user=  request.user
        try:
            FedPersonel = get_object_or_404(FederationPersonel, user = user)
            FedPersonel.FederationName = request.POST["FederationName"]
            FedPersonel.dateSelected = datetime.now()
            FedPersonel.save()
        except:
            FedPersonel = FederationPersonel.objects.create(
                user = user,
                FederationName = request.POST["FederationName"],
                dateSelected = datetime.now()
            )
            
        AlertGovManager(request, user,request.POST["userEmail"],{"first_name": request.POST["userName"], "last_name":request.POST["userSurname"]},FedPersonel)
        messages.success(request, "Great you have selected your feration, you may continue with your application")
        #alert Governance manager by email
        if FedPersonel.PersonelPhone == None:
            messages.warning(request, "please update your phone number and start again with the application process.")
            return redirect("account")
        return redirect("CreateApplication")
    
    
    
    
    
@api_view(['GET'])
def checkDateAp(request, date):
    try:
        provided_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=400)

    current_date = datetime.now().date()
    difference = (provided_date - current_date).days

    if difference >= 30:
        return Response({'isValid': True})
    else:
        return Response({'isValid': False})
    
def checkDate(date):
    try:
        provided_date = datetime.strptime(date, '%Y-%m-%d').date()
    except ValueError:
        return Response({'error': 'Invalid date format'}, status=400)

    current_date = datetime.now().date()
    difference = (provided_date - current_date).days

    if difference >= 30:
        return Response({'isValid': True})
    else:
        return Response({'isValid': False})
    
    
@login_required
def allowAppTake(request):
    print("request: ", request)
    if request.method == 'POST':
        try:
            application = get_object_or_404(Application, pk = request.POST["applicationId"])
            msg = ''

            if request.POST["action"] == "Allowed":
                application.is_App_taking = True
                msg ='Athletes, officials, and commitee members are allowed to make colors application.'

                messages.success(request, msg)
            elif request.POST["action"] == "DisAllowed":
                application.is_App_taking = False
                msg ='Athletes, officials, and commitee members are not longer allowed to make colors application.'
            
                messages.error(request, msg)  
            application.save()
        except:
            messages.error(request, "Something went wrong please try again")
            pass
        return redirect("Application_review", applicationId = application.ApplicationId)
    else:
        messages.error(request, "Something went wrong please try again")
        
        return redirect("home")
    
    
        
    
    
    
    
    
    
def Select_Event(request):
    
    
    openApplications = Application.objects.filter(is_App_taking = True)
    
    if request.method == 'GET':
       # messages.success(request, "The test mes")
        return render(request, 'MyApp/Select_Event.html', {"openApplications": openApplications})
    pass

    if request.method =='POST':
        
        application = None
        
        try:
            application = get_object_or_404(Application, pk = request.POST["ApplicationId"])
            
        except:
            messages.error(request, "The application you tried to access was not found.")
            return redirect("Select_Event")
        
        
        
@login_required
def Represantation(request, applicationId):
    
    application = None
    try:
        application  = get_object_or_404(Application, pk = applicationId)
        
    except:
        messages.error(request, "The application you tried to acces was not found")
        return redirect("home")
    
    return render(request, 'MyApp/chooseRepType.html', {"application":application})
  
