from django.shortcuts import render
from MyApp.models import *
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages

from MyApp.views import countObj

def ApprovedApplications(request):
    
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
    
    

@login_required
def awardingColors(request, applicationId):
    try:
        application = get_object_or_404(Application, pk=applicationId)
        print(f"Application {applicationId} fetched successfully")
    except Exception as e:
        messages.error(request, "The application you tried to modify does not exist for unknown reasons")
        print(f"Error fetching application {applicationId}: {e}")
        return redirect("home")
    
    if request.method == 'GET':
        informationOBJ = {
            "application": application,
        }
        return render(request, 'awarding/awardingColors.html', informationOBJ)

    if request.method == 'POST':
        print(f"POST request received for application ID: {applicationId}")

        application.ApplicationStatus = "Active"
        application.Step = "Active"
        try:
            application.Committee = get_object_or_404(CommitteeMember, user=request.user)
            print(f"Committee member set for application {applicationId}")
        except Exception as e:
            messages.error(request, "You are not allowed to take this action")
            print(f"Error setting committee member: {e}")
            return redirect('home')

        application.save()
        print(f"Application {applicationId} updated and saved successfully")
        messages.success(request, "Application status updated successfully.")
        return redirect("ApprovedApplications")  # Ensure this URL name is correct
    else:
        print(f"Invalid request method: {request.method}")
        messages.error(request, "Invalid request method.")
        return redirect("home")
       
        