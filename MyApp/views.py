from django.shortcuts import render,redirect, get_object_or_404
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
from .functions import *
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse




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

    try:
        federationPersonel = get_object_or_404(FederationPersonel, user = user)
        if federationPersonel.FederationName == None:
            messages.error(request, "Please select your federation, in order to add a new application.")
            return redirect("chooseFederation")
    except:
        messages.error(request, "Please select your federation")
        return redirect("chooseFederation")
    
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
            
   
        
        return render(request, 'MyApp/CreateApp.html', {"federationPersonel":federationPersonel})
    
    if request.method == 'POST':
       
        application = Application.objects.create(
                user = user,
                FederationPersonel = federationPersonel,
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
        valid = checkDate(application.StartDate.day,application.StartDate.month,application.StartDate.year)
        if valid:
            messages.success(request, 'The information has been saved successfully, proceed to add the team officials.')
                
                
                
            return redirect("addTeamOfficial", applicationId= application.ApplicationId)
        else:
            application.delete()
            messages.error(request, "you can only make applications for events 30 days prior for a successfull submission")
            return redirect("CreateApplication")
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
      
        Repps = Represantative.objects.filter(application = application)
        
        if Thefunctions.getObjectCount(Repps) == 0:
            application.Step = 'AddRepp'
            application.save()
        if request.POST["AcceptanceofTeamAppointment"] == 'yes':
            isAceptencSubmited = True
            
        if request.POST["IDCopySubmited"] == 'yes':
            isIdSubmit = True
            
        Rep = Represantative.objects.create(     
          
           application = application,
            FirstName = request.POST['FirstName'],
            Surname = request.POST['Surname'],
            Gender = request.POST['Gender'],
            PhoneNumber = request.POST['PhoneNumber'],
            Email = request.POST['Email'],
            City = request.POST['City'],
            Province = request.POST["Province"],
            RepresatativeType = request.POST["RepresatativeType"],
            IDCopySubmited = isIdSubmit,
            AcceptanceofTeamAppointment = isAceptencSubmited
            
        )
        messages.success(request, "Team represantative add successfully")
        
        
            
        return redirect("AddRepp",applicationId=application.ApplicationId)


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
        return redirect("AddRepp", applicationId = application.ApplicationId)
            

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
def Add_Committee_Member(request, applicationId):
    application = get_object_or_404(Application, pk=applicationId)
    CommitteeMembers = CommitteeMember.objects.filter(application = application)
    
    if request.method == 'GET':
        
        return render(request, 'MyApp/Add_Committee_Member.html',{"CommitteeMembers":CommitteeMembers,"application":application})
    
    if request.method == 'POST':
        
        if Thefunctions.getObjectCount(CommitteeMembers) == 0:
            application.Step = 'Add_Committee_Member'
            application.save()
        committeeMember = CommitteeMember.objects.create(
            
            application = application,
         
            FirstName = request.POST['FirstName'],
            Surname = request.POST['Surname'],
            Gender = request.POST['Gender'],
            Email = request.POST["Email"],
            PhoneNumber = request.POST["PhoneNumber"],
            City = request.POST["City"],
            Province = request.POST["Province"]
        )
        messages.success(request, "Committee member added successfully")
        return redirect("Add_Committee_Member",applicationId=application.ApplicationId)

@login_required
def update_CommiteeMember(request, CommitteeMemberId):
    
    committeeMember = get_object_or_404(CommitteeMember, pk=CommitteeMemberId)
    application = committeeMember.application

    if request.method =='GET':
        
        return render(request, 'MyApp/update_CommiteeMember.html', {"committeeMember":committeeMember,"application":application})
    
    if request.method =='POST':
        
        numUpdates = 0
        
        if committeeMember.FirstName != request.POST["FirstName"]:
            committeeMember.FirstName = request.POST["FirstName"]
            numUpdates += 1
            
        if committeeMember.Surname  != request.POST["Surname"]:
            
            committeeMember.Surname = request.POST["Surname"]
            numUpdates += 1
        
        if request.POST["Gender"] != 'none':
            if committeeMember.Gender != request.POST["Gender"]:
                committeeMember.Gender = request.POST["Gender"]
                numUpdates += 1
                
        if committeeMember.Email != request.POST["Email"]:
            
            committeeMember.Email = request.POST["Email"]
            numUpdates += 1
            
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
            
            committeeMember.save()
            messages.success(request, "The changes were saved successfully.")
        else:
            messages.info(request, "No changes made on the record.")
            
        
        return redirect("Add_Committee_Member", applicationId=application.ApplicationId)            

@login_required

def CommitteeMemberDetails(request, MemberId):
    
    obj = get_object_or_404(CommitteeMember, pk= MemberId)
    print(obj)
    
    return render(request, 'MyApp/CommitteeMemberDetails.html', {"obj":obj})
         
   
    
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
                messages.success(request, "Changes saved successfully "+str(numUpdates))
                application.save()
            else:
                messages.error(request, 'No changes made')   
                
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
            
        informationOBJ = {
            "numCommitee":numCommitee,
            "numOfficials":numOfficials,
            "application":application,
            "represantatives":represantatives,
            "CommitteeMembers":CommitteeMembers,
            "teamOfficials":teamOfficials,
            "numApplicants":numApplicants,
            "FederationPersonel":fedPerson, 
            "apparel":apparel
            }
        return render(request, 'MyApp/Application_review.html', informationOBJ)
    
    if request.method == 'POST':
        
        valid = checkDate(application.StartDate.day,application.StartDate.month,application.StartDate.year)
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
    
def Committee(request, applicationId):
    
    application = get_object_or_404(Application,pk = applicationId)
    commitee = CommitteeMember.objects.filter(application = application)
    
    if request.method =='GET':
        
        return render(request, 'MyApp/Committee.html', {"application":application, "commitee":commitee})
    
def Documents(request, applicationId):
    
    
    application = get_object_or_404(Application,pk = applicationId)
    if request.method == 'GET':
        
        return render(request, 'MyApp/Documents.html', {"application":application})
    
    
# detalis pages 
def teamOfficialDetails(request, teamOfficialId):
    
    teamOfficial = get_object_or_404(TeamOfficial, pk=teamOfficialId)
    
    application = teamOfficial.application
    
    return render(request, 'MyApp/teamOfficialDetails.html', {"teamOfficial":teamOfficial,"application":application})
            
def represantativeDetails(request, represantativeId):
    
    represantative = get_object_or_404(Represantative, pk=represantativeId)
    application = represantative.application
    return render(request, 'MyApp/represantativeDetails.html',{"represantative":represantative,"application":application})
            
def CommitteeMemberDetails(request, committeeMemberId):
    
    committeeMember = get_object_or_404(CommitteeMember, pk = committeeMemberId)
    application = committeeMember .application
    
    return render(request, 'MyApp/CommitteeMemberDetails.html', {"committeeMember":committeeMember,"application":application})   
@login_required
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
                ActiveApplication = None 
                pass  
    
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
            
        AlertGovManager(request, user,request.POST["userEmail"],{"first_name": request.POST["userName"], "last_name":request.POST["userSurname"]},FedPersonel)
        messages.success(request, "Great you have selected your feration, you may continue with your application")
        #alert Governance manager by email
        if FedPersonel.PersonelPhone == None:
            messages.warning(request, "please update your phone number and start again with the application process.")
            return redirect("account")
        return redirect("CreateApplication")
    
    
    

def AlertGovManager(request, user, to_email, coloresUser, federationPersonel):
    print(f"To user: {user.username}")
    mail_subject = "Colours application  representative."
    message = render_to_string("MyApp/AlertGovManager.html",{
        'federationPersonel':federationPersonel,
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
        
    except:
        pass        

    
    
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


