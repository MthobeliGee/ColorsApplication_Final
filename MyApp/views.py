from django.shortcuts import render,redirect, get_object_or_404
from .models import Application,Represantative, CommitteeMember, TeamOfficial,Thefunctions
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from datetime import datetime



def Home(request):
    application  = None
    if request.user.is_authenticated:
        
        try:
            application = get_object_or_404(Application, user = request.user, ApplicationStatus='Oncreate')
        except:
                try:
                    application = get_object_or_404(Application, user = request.user, ApplicationStatus='Complete')
                except:
                    pass
            
            
        
   
    return render(request,'MyApp/Home.html', {"application":application})
@login_required
def CreateApplication(request):
    user = request.user
    if request.method == 'GET':
        
        
        
        return render(request, 'MyApp/CreateApp.html')
    
    if request.method == 'POST':
        traveldateTime = request.POST["TravelDate"]+" "+ request.POST["TravelTime"]
        application = Application.objects.create(
                user = user,
        
                EventName = request.POST['EventName'],
                StartDate = request.POST['StartDate'],
                EndDate = request.POST['EndDate'],
                HostCity = request.POST['HostCity'],
                HostProvince = request.POST['HostProvince'],
                NumberOfTeam = request.POST['NumberOfTeam'],
                MethodOfSelection = request.POST['MethodOfSelection'],
                SelectionApprovedDate = request.POST['SelectionApprovedDate'],
                TravelDateTime = traveldateTime,
                ModeOfTravel = request.POST['ModeOfTravel'],
        
       )
    messages.success(request, 'The information has been saved successfully, proceeed to add the team officials.')
         
        
        
    return redirect("addTeamOfficial", applicationId= application.ApplicationId)
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
    
    
    
    
    
    
def ViewDetails(request, ApplicationId):
    
    application = get_object_or_404(Application,pk=ApplicationId)
    print(application)
    
    return render(request, 'MyApp/ViewDetails.html',{"application":application})

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
        
        
        
        

def RepDetails(request, RepresantativeId):
    
    Rep =get_object_or_404(Represantative, pk= RepresantativeId)
    print(Rep)
    
    return render (request, 'MyApp/RepDetails.html',{"Rep":Rep}) 

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


def CommitteeMemberDetails(request, MemberId):
    
    obj = get_object_or_404(CommitteeMember, pk= MemberId)
    print(obj)
    
    return render(request, 'MyApp/CommitteeMemberDetails.html', {"obj":obj})
         
    
    
    
def Upload_Documents(request, applicationId):
    
    application = get_object_or_404(Application, pk = applicationId)
    application.Step = 'Upload_Documents'
    application.save()
    if request.method == 'GET':
        
        return render(request, 'MyApp/Upload_Documents.html',{"application":application}) 
    
    if request.method == 'POST':
        
        application.RegulationsInterestDeclaration = request.POST["RegulationsInterestDeclaration"]
        application.SelectionCriteriaProtocols = request.POST["SelectionCriteriaProtocols"]
        application.GeneralRegulationSelectionProcedure = request.POST["GeneralRegulationSelectionProcedure"]
        application.TeamOfficialDuties = request.POST["TeamOfficialDuties"]
        application.HighPerformancePlan = request.POST["HighPerformancePlan"]
        application.EventInvitation = request.POST["EventInvitation"]
        application.DocumentationOfSelectionSubmitted = request.POST["DocumentationOfSelectionSubmitted"]
        
        application.save()
        
        messages.success(request, "Documents uploaded successfully, please proceed to accept code of conduct terms.")
        
        return redirect("termsAndConditions", applicationId = application.ApplicationId)
    

    
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
        
        
    
    
def Application_review(request, applicationId):
    
    application = get_object_or_404(Application, pk=applicationId)
    represantatives = Represantative.objects.filter(application = application)
    CommitteeMembers = CommitteeMember.objects.filter(application = application)
    teamOfficials = TeamOfficial.objects.filter(application= application)
    if application.Step != 'Application_review':
        application.Step = 'Application_review'
        application.save()
    return render(request, 'MyApp/Application_review.html', {"application":application,"represantatives":represantatives,"CommitteeMembers":CommitteeMembers,"teamOfficials":teamOfficials})
    
    
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
        
   
        
   
        