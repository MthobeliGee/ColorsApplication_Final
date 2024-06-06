from django.db import models
from datetime import date, datetime
from django.utils import timezone
from django.contrib.auth.models import User 
from manage_personnel.models import *
    


class Federation(models.Model):
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
<<<<<<< HEAD
    FederationId = models.AutoField(primary_key=True, null= False, blank=False)
    FederationPersonel = models.ForeignKey(FederationPersonel,blank=True,null=True,on_delete=models.CASCADE)
    FederationName = models.TextField(blank=True, null = True)
    dateSelected = models.DateField(default=datetime.now())
    year = models.IntegerField()
    FederationEmail = models.TextField(null = True, blank= True)
    is_Gov_approved = models.CharField(max_length=30, default='Pending')
    date_requested = models.DateTimeField(default =datetime.now())
    date_approved = models.DateTimeField(default =datetime.now())

    
    
class ApplicantTeams(models.Model):
    
    ApplicantTeamsId = models.AutoField(primary_key=True, blank=False, null = False, )
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    Federation = models.ForeignKey(Federation, on_delete=models.CASCADE)
    teams = models.TextField()
    
    
    
    
    


=======
    FederationName = models.CharField(max_length=255,blank=True,null=True)
    dateSelected = models.DateField(default=timezone.now())
    PersonelPhone = models.CharField(max_length=255 , null=True, blank=True)
    PersonelGender = models.CharField(max_length=6,null=True, blank=True)
    Status = models.CharField(max_length=20,default="Pending")
>>>>>>> 63f1979025f70cff35c98ec0d995a34b184f4a6e


class FedDocuments(models.Model):
    DocumentsId = models.AutoField(primary_key=True, auto_created=True, blank=False,null=False)
    FederationPersonel = models.ForeignKey(FederationPersonel,blank=True,null=True,on_delete=models.CASCADE)
    RegulationsInterestDeclaration  = models.FileField(blank=False,null=False,upload_to='MyApp/Docs')
    RegulationsInterestDeclaration  = models.FileField(blank=False,null=False,upload_to='MyApp/Docs')
    SelectionCriteriaProtocols = models.FileField(blank=False,null=False,upload_to='MyApp/Docs')
    GeneralRegulationSelectionProcedure  =models.FileField(blank=False,null=False,upload_to='MyApp/Docs')
    DocumentationOfSelectionSubmitted = models.FileField(blank=False,null=False,upload_to='MyApp/Docs')
    TeamOfficialDuties = models.FileField(blank=False,null=False,upload_to='MyApp/Docs')
    AcceptanceOfTeamAppointment = models.FileField(blank=False,null=False,upload_to='MyApp/Docs')
    HighPerformancePlan = models.FileField(blank=False,null=False,upload_to='MyApp/Docs')
    
    
    DateAdded = models.DateTimeField(default = datetime.now())
    Year = models.CharField(max_length = 12, default = str(datetime.now().year))
    
class CommitteeMember(models.Model):
    
    CommitteeMemberId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    Id_number = models.CharField(max_length = 13, null =True, blank=True)
    FirstName = models.CharField(max_length=255)
    Surname = models.CharField(max_length=255)
    Gender = models.CharField(max_length=255)
    Email = models.CharField(max_length=255, default="email")
    PhoneNumber = models.CharField(max_length=255, default="number")
    City = models.CharField(max_length=255, default="city")
    Province = models.CharField(max_length=255, default="KwaZulu-Natal")
    position = models.CharField(max_length=100, )
    status = models.CharField(max_length= 30, default="Active")
    is_Chairperson = models.BooleanField(default =False)
    is_deleted = models.BooleanField(default =False)
    is_history = models.BooleanField(default =False)
    DateAdded  = models.DateTimeField(default=datetime.now())
    
    
# Create your models here.
class Application(models.Model):
    ApplicationId = models.AutoField(primary_key=True)
    Committee = models.ForeignKey(CommitteeMember,blank=True,null=True,on_delete=models.DO_NOTHING)
    
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    
    Federation = models.ForeignKey(Federation,blank=True,null=True,on_delete=models.CASCADE)
    
    EventName = models.CharField(max_length=255)
    StartDate = models.DateTimeField(max_length=255)
    EndDate = models.DateTimeField(max_length=255)
    HostCity = models.CharField(max_length=255)
    HostProvince =models.CharField(max_length=255)
    ReportSubmitAgreement = models.BooleanField(default=False)
    NumberOfTeam = models.IntegerField(default=0)
    MethodOfSelection = models.CharField(max_length=255)
    SelectionApprovedDate = models.DateField(max_length=255)
    TravelDateTime = models.DateTimeField(max_length=255)
   
    CodeOfConductAcceped = models.BooleanField(default=False)
    AcceptanceOfTeamAppointment = models.CharField(max_length=300, default='NotProvided')
    EventInvitation  = models.CharField(max_length=300, default='NotProvided')
    ApplicationDate  = models.DateTimeField(default=datetime.now())
    Step = models.CharField(max_length=255, default='start')
    ApplicationStatus = models.CharField(max_length=255, default='Oncreate')
    isHistory = models.BooleanField(default=False)
    DateCreated = models.DateTimeField(default=datetime.now())
    DeclineReason = models.TextField(blank=True, null=True)
    CancelReason = models.TextField(blank=True, null=True)
<<<<<<< HEAD
    is_App_taking = models.BooleanField(default = False)
    ApplicantsClosingDate = models.DateTimeField(default=datetime.now())
=======
    LateAppMotivation = models.TextField(max_length=255)
    
>>>>>>> 63f1979025f70cff35c98ec0d995a34b184f4a6e
    ApparelLetters = models.CharField(max_length=300, blank=True, null=True)
    is_lateApplication = models.BooleanField(default=False)


class Apparel(models.Model):
    
    ApparelId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    application = models.ForeignKey(Application,blank=True,null=True,on_delete=models.CASCADE)
    letter  = models.CharField(max_length=300, default='NotProvided')
    DateAdded = models.DateTimeField(default=datetime.now())
    Status = models.CharField(max_length=20,default="Approved")
    DateCreated = models.DateTimeField(default=datetime.now())
    
    
    
    
class SportsPerson(models.Model):
    SportsPersonId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    
    Id_number = models.CharField(max_length = 13, null =True, blank=True)
    FirstName = models.CharField(max_length=255)
    Surname =models.CharField(max_length=255)
    Gender = models.CharField(max_length=255)
   
    PhoneNumber = models.CharField(max_length=255)
    Email = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
    Province = models.CharField(max_length=255)
    Date = models.DateTimeField(auto_now=False, auto_now_add=True) 
    RepresanativeLeve = models.CharField(max_length=255, default ='1')
 
    IDCopySubmited = models.BooleanField(default=False,blank=False,null=False)
    AcceptanceofTeamAppointment = models.BooleanField(default=False,blank=False,null=False)

    is_IdNumberValidated = models.BooleanField(default=False)
    is_parent =models.BooleanField(default = False)
   
    
    
    
class ApplicantApplication(models.Model):
    ApplicantApplicationId = models.AutoField(primary_key=True, blank=False, null=False)
    Application = models.ForeignKey(Application,blank=True,null=True,on_delete=models.CASCADE)
    SportsPerson = models.ForeignKey(SportsPerson,blank=True,null=True,on_delete=models.CASCADE)
    is_terms_accepted = models.BooleanField(default  = False)
    is_deleted = models.BooleanField(default=False)
    RepresatativeType = models.CharField(max_length=50, default='Athlete')
    RepresatativeLevel = models.CharField(max_length=50, default='Junior')
    status = models.CharField(max_length= 30, default="OnCreate")
    declineReason = models.TextField(blank=True, null=True)
    
    


class TeamOfficial(models.Model):
    
    TeamOfficialId = models.AutoField(primary_key=True, auto_created=True, null=False, blank=False)
    application = models.ForeignKey(Application,blank=True,null=True,on_delete=models.CASCADE)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    
    Id_number = models.CharField(max_length = 13, null =True, blank=True)
    FirstName = models.CharField(max_length=100, blank=False,null=False)
    LastName = models.CharField(max_length=100, blank=False,null=False)
    Gender = models.CharField(max_length=30, null=False, blank=False)
    PhoneNumber = models.CharField(max_length=255, default="number")
    Email = models.CharField(max_length=255, default="email")
    
    Designation = models.CharField(max_length=100, blank=False,null=False)
    IDCopySubmited = models.BooleanField(default=False) 
    AcceptanceofTeamAppointment  = models.BooleanField(null=False, blank=False, default=False)
    is_terms_accepted = models.BooleanField(default  = False)
    
    status = models.CharField(max_length= 30, default="OnCreate")
    

class Thefunctions():
    
    def getObjectCount(list):
        
        numObj = 0
        for obj in list:
            numObj += 1
            
        return numObj 

    
    
    


    
    

   