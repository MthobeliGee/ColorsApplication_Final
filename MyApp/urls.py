from . import views
from django.urls import path

urlpatterns = [
    path('',views.Home, name="home"),
    path('CreateApplication', views.CreateApplication, name="CreateApplication"),
    path('ViewDetails/<int:ApplicationId>', views.ViewDetails, name="ViewDetails"),
    path('UpdateDetails/<int:ApplicationId>', views.UpdateDetails,name="UpdateDetails"),
    path('AddRepp/<int:applicationId>', views.AddRepp, name="AddRepp"),
    path('RepDetails/<int:RepresantativeId>/', views.RepDetails,name="RepDetails"),
    path('Add_Committee_Member/<int:applicationId>', views.Add_Committee_Member, name="Add_Committee_Member"),
    path('CommitteeMemberDetails/<int:MemberId>/', views.CommitteeMemberDetails,name="CommitteeMemberDetails"),
    path('addTeamOfficial/<int:applicationId>',views.addTeamOfficial, name="addTeamOfficial"),
    path('update_team_official/<int:officialId>', views.update_team_official, name="update_team_official"),
    path('remove_team_official/<int:officialId>', views.remove_team_official, name="remove_team_official"),
    path('update_Representative/<int:represantativeId>',views.update_Representative, name="update_Representative"),
    path('remove_Representative/<int:represantativeId>',views.remove_Representative, name="remove_Representative"),
    path('update_CommiteeMember/<int:CommitteeMemberId>', views.update_CommiteeMember, name="update_CommiteeMember"),
    path('Upload_Documents/<int:applicationId>', views.Upload_Documents, name="Upload_Documents"),
    path('Remove_CommitteeMember/<int:memberId>', views.Remove_CommitteeMember, name="Remove_CommitteeMember"),
    path('termsAndConditions/<int:applicationId>',views.termsAndConditions, name="termsAndConditions"),
    path('Application_review/<int:applicationId>',views.Application_review, name="Application_review"),
    path('teamOfficialDetails/<int:teamOfficialId>', views.teamOfficialDetails, name="teamOfficialDetails"),
    path('represantativeDetails/<int:represantativeId>', views.represantativeDetails, name="represantativeDetails"),
    path('ContinueApplication/<int:applicationId>',views.ContinueApplication, name="ContinueApplication"),
    path('CommitteeMemberDetails/<int:committeeMemberId>', views.CommitteeMemberDetails, name="CommitteeMemberDetails"),
    path('Officials/<int:applicationId>', views.Officials, name="Officials"),
    path('Applcants/<int:applicationId>', views.Applcants, name="Applcants"),
    path('Committee/<int:applicationId>', views.Committee, name="Committee"),
    path('Documents/<int:applicationId>', views.Documents, name="Documents"),
    path('my_applications', views.my_applications, name="my_applications"),
    path('Applications', views.Applications, name="Applications"),
    path('Approved', views.Approved, name="Approved"),
    path('History', views.History, name="History"),
    path('Active', views.Active, name="Active"),
    path('chooseFederation', views.chooseFederation, name="chooseFederation")
    
    
]
