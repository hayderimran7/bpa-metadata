from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class Affiliation(models.Model):
    """
    Affiliation
    """
    name = models.CharField(max_length=20, primary_key=True)
    description = models.CharField(max_length=200, blank=True)

    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    """
    User's Profile. Expand this to add additional user information. 
    """
    
    user = models.OneToOneField(User)
    affiliation = models.ForeignKey(Affiliation, null=True)

    def __unicode__(self):
        return "{} {}".format(self.user, self.affiliation)
    
def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfile.objects.get_or_create(user=instance)  
 
post_save.connect(create_user_profile, sender=User) 
