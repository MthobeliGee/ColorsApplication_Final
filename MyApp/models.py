from django.db import models
from datetime import date, datetime
from django.contrib.auth.models import User 

class FederationPersonel(models.Model):
    #I am last adding this class on the user but wondering about the other part where I get the applications by user, fix that too 
    PersonelId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    FederationName = models.CharField(max_length=255,blank=True,null=True)
    dateSelected = models.DateField(default=datetime.now())
    PersonelPhone = models.CharField(max_length=255)
    PersonelGender = models.CharField(max_length=6,null=True, blank=True)
    Status = models.CharField(max_length=20,default="Pending")



# Create your models here.
class Application(models.Model):
    ApplicationId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    
    FederationPersonel = models.ForeignKey(FederationPersonel,blank=True,null=True,on_delete=models.CASCADE)
    
    EventName = models.CharField(max_length=255)
    StartDate = models.DateTimeField(max_length=255)
    EndDate = models.DateTimeField(max_length=255)
    HostCity = models.CharField(max_length=255)
    HostProvince =models.CharField(max_length=255)
    ReportSubmitAgreement = models.BooleanField(default=False)
    NumberOfTeam = models.IntegerField()
    MethodOfSelection = models.CharField(max_length=255)
    SelectionApprovedDate = models.DateField(max_length=255)
    TravelDateTime = models.DateTimeField(max_length=255)
    ModeOfTravel = models.CharField(max_length=255)
    CodeOfConductAcceped = models.BooleanField(default=False)
    RegulationsInterestDeclaration  = models.CharField(max_length=300, default='NotProvided')
    RegulationsInterestDeclaration  = models.CharField(max_length=300, default='NotProvided')
    SelectionCriteriaProtocols = models.CharField(max_length=300, default='NotProvided')
    GeneralRegulationSelectionProcedure  =models.CharField(max_length=300, default='NotProvided')
    DocumentationOfSelectionSubmitted = models.CharField(max_length=300, default='NotProvided')
    TeamOfficialDuties = models.CharField(max_length=300, default='NotProvided') 
    AcceptanceOfTeamAppointment = models.CharField(max_length=300, default='NotProvided')
    HighPerformancePlan = models.CharField(max_length=300, default='NotProvided')
    EventInvitation  = models.CharField(max_length=300, default='NotProvided')
    ApplicationDate  = models.DateTimeField(default=datetime.now())
    Step = models.CharField(max_length=255, default='start')
    ApplicationStatus = models.CharField(max_length=255, default='Oncreate')
    isHistory = models.BooleanField(default=False)
    DateCreated = models.DateTimeField(default=datetime.now())
    DeclineReason = models.TextField(blank=True, null=True)
    CancelReason = models.TextField(blank=True, null=True)
    
    ApparelLetters = models.CharField(max_length=300, blank=True, null=True)


class Apparel(models.Model):
    
    ApparelId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    application = models.ForeignKey(Application,blank=True,null=True,on_delete=models.CASCADE)
    letter  = models.CharField(max_length=300, default='NotProvided')
    DateAdded = models.DateTimeField(default=datetime.now())
    Status = models.CharField(max_length=20,default="Approved")
    DateCreated = models.DateTimeField(default=datetime.now())
    
    
    
    
class Represantative(models.Model):
    RepresantativeId = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application,blank=True,null=True,on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=255)
    Surname =models.CharField(max_length=255)
    Gender = models.CharField(max_length=255)
    Event = models.CharField(max_length=255)
    PhoneNumber = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    Province = models.CharField(max_length=255)
    Date = models.DateTimeField(auto_now=False, auto_now_add=True)
    RepresanativeLeve = models.CharField(max_length=255)
    Duration = models.CharField(max_length=255)
    IDCopySubmited = models.BooleanField(default=False,blank=False,null=False)
    AcceptanceofTeamAppointment = models.BooleanField(default=False,blank=False,null=False)
    RepresatativeType = models.CharField(max_length=255, default='Junior')
    

class CommitteeMember(models.Model):
    
    CommitteeMemberId = models.AutoField(primary_key=True)
    application = models.ForeignKey(Application,blank=True,null=True,on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=255)
    Surname = models.CharField(max_length=255)
    Gender = models.CharField(max_length=255)
    Email = models.CharField(max_length=255, default="email")
    PhoneNumber = models.CharField(max_length=255, default="number")
    City = models.CharField(max_length=255, default="city")
    Province = models.CharField(max_length=255, default="province")
    
class TeamOfficial(models.Model):
    TeamOfficialId = models.AutoField(primary_key=True, auto_created=True, null=False, blank=False)
    application = models.ForeignKey(Application,blank=True,null=True,on_delete=models.CASCADE)
    FirstName = models.CharField(max_length=100, blank=False,null=False)
    LastName = models.CharField(max_length=100, blank=False,null=False)
    Gender = models.CharField(max_length=30, null=False, blank=False)
    Designation = models.CharField(max_length=100, blank=False,null=False)
    IDCopySubmited = models.BooleanField(default=False) 
    AcceptanceofTeamAppointment  = models.BooleanField(null=False, blank=False, default=False)

class Thefunctions():
    
    def getObjectCount(list):
        
        numObj = 0
        for obj in list:
            numObj += 1
            
        return numObj 

    
    
    


    
    

   