from django.db import models
from MyApp.models import *
from datetime import date, datetime
from django.contrib.auth.models import User 






class FederationPersonel(models.Model):
    #I am last adding this class on the user but wondering about the other part where I get the applications by user, fix that too 
    PersonelId = models.AutoField(primary_key=True)
    user = models.ForeignKey(User,blank=True,null=True,on_delete=models.CASCADE)
    first_name = models.TextField()
    last_name= models.TextField()
    id_number = models.CharField(max_length=13)
    Gender = models.CharField(max_length=6,null=True, blank=True)
    email = models.TextField()
    Phone = models.CharField(max_length=255 , null=True, blank=True)
    Status = models.CharField(max_length=20,default="Pending")
    DateAdded = models.DateTimeField(default = datetime.now())

