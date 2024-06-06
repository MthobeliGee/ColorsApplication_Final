from datetime import datetime
import calendar
import random
from django.contrib.auth.models import User
from .models import *
from django.shortcuts import  get_object_or_404
from LoginManager.tokens import account_activation_token
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str


def checkDate(dd, mm, yyyy):
    isValid = False
    
    CurrentYear = datetime.now().year
    currentMonth = datetime.now().month
    currentday = datetime.now().day
    lastDayMonth = calendar.monthrange(datetime.now().year,datetime.now().month)[1]
    bMonths = mm - currentMonth
    bMonths = mm - currentMonth
    bMonths = mm - currentMonth
    
    if CurrentYear < yyyy and bMonths > 1:
        print("1")
        isValid = True
    if CurrentYear <= yyyy and bMonths <= 1:
        print("2")
        if bMonths > 1:
            print("4")
            isValid = True
        if bMonths == 1:
            print("5")
            days = dd+(lastDayMonth - currentday)
            
            if days >= 30:
                print("6")
                isValid = True
        if bMonths <1:
            print("7")
            print("dd: ", dd)
            if mm != currentMonth:
                days = dd+(lastDayMonth - currentday)
                if days >= 30:
                    print(8)
                    isValid = True
            else:
                print("8")
                if dd >= 30:
                    print("9")
                    isValid = True
                   
                   
    return isValid


valid = checkDate(1,12,2022)

print(valid)
        
            
def NewPassword():
    Characters = list('abcdefghiklmnopqrstuvwxyz')
    upperChar = 'abcdefghiklmnopqrstuvwxyz'.upper()
    Characters.extend(upperChar)
    numbers = '0123456789'
    Characters.extend(numbers)
    specialCar = '!@#$%^&*'
    Characters.extend(specialCar)
    NewPassword = ''
    for x in range(8):
        NewPassword += random.choice(Characters)   
    return NewPassword       
            
    
        
def newCommiteeUser(committeeMember): 
    password = NewPassword()
    try:
        user = User.objects.create_user(first_name =committeeMember.FirstName,last_name =committeeMember.Surname,username = committeeMember.Email.lower(),email =committeeMember.Email.lower(), password =password)
        user.is_active = False
        user.is_staff = True
        user.save()  
    except:
        user = None
        pass
    return (user, password)
        
                             
def alertNewCommittee(request, user, password):
    print("user_committee: ", user)
    committeeMember = get_object_or_404(CommitteeMember, user = user)
    mail_subject = "Acivate your account."
    message = render_to_string("MyApp/alerts/alert_NewCommittee.html",{
        'committeeMember':committeeMember,
        'password':password,
        'user':user,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    try:
        send_mail(mail_subject,f"{message}"  ,'',[f'{user.email}'], fail_silently=False)
        return True
    except:
        return False       


def is_DateValid(provided_date):
    print()
    print((provided_date.date() - datetime.now().date()).days)
    if (provided_date.date() - datetime.now().date()).days >= 30:
        return True
    else:
        return False
    
    
def demoteCommittee(request, position):
    
    print("DEMOTING!")
    print()
    commettee = None
    try:
        commettee = get_object_or_404(CommitteeMember,position = position )
       
        commettee.position = "Demoted"
        commettee.is_history = True
        if commettee.user == None:
            commettee.delete()
        else:
            commettee.user.is_staff = False
            commettee.user.save()
            if commettee.position =="Chairperson":
                commettee.is_Chairperson = False
        
            commettee.save()
        
            alertDemotedCommittee(request, commettee.CommitteeMemberId)
    except:
         pass
   
    
def alertDemotedCommittee(request, commetteeId):
    committeeMember = get_object_or_404(CommitteeMember, pk = commetteeId)
    mail_subject = "Committee membership."
    message = render_to_string("MyApp/alerts/alertDemotedCommittee.html",{
        'committeeMember':committeeMember,
        'domain': get_current_site(request).domain,
        "protocol": 'https' if request.is_secure() else 'http'
    })
    try:
        send_mail(mail_subject,f"{message}"  ,'',[f'{committeeMember.Email}'], fail_silently=False)
        return True
    except:
        return False       


def is_super_or_Chair(request):
    
    isSuperOrChair = False
    
    user = request.user
    if user.is_superuser:
        isSuperOrChair = True
    elif user.is_staff:
        try:
            BoardMembership = get_object_or_404(CommitteeMember, user = user)
            if BoardMembership.position == 'Chairperson':
                isSuperOrChair = True
        except:
            pass
        
    return isSuperOrChair
            