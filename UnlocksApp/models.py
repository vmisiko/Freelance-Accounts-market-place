from django.db import models
from django.conf import settings


# Create your models here.
cat_choices = {
    ("Chegg","Chegg Unlocks"),
    ("CourseHero", "CourseHero Unlocks"),
    ("Scrbd", "Scrbd Unlocks")
}
 
logcat_choices = {
    ("Chegg","Chegg Logins"),
    ("CourseHero", "CourseHero Logins"),
    ("Scrbd", "Scrbd Logins"),
    ("Turnitin","Turnitin Logins"),
    ("Grammarly", "Grammarly Premium"),
    ("Netflix Logins", "Netflix Logins"),
    ("Nord", "Nord VPN"),
    ("DSTV", "DSTV")
}

class Unlocks(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE, blank=True, null=True)
    full_Names = models.CharField(max_length= 500 )
    category = models.CharField(choices = cat_choices, max_length=20)
    email = models.EmailField()
    Url = models.URLField()
    other = models.CharField(max_length= 500 , blank=True, null=True)
    status = models.BooleanField(default=False)

class Logins(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete = models.CASCADE)
    full_Names = models.CharField(max_length= 500 )
    category = models.CharField(choices = logcat_choices, max_length=20)
    email = models.EmailField()
    other = models.CharField(max_length= 500, blank=True, null=True)
    status = models.BooleanField(default=False)

    
    

