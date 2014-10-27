from django.db import models
from django.contrib.auth.models import User
import shortuuid
from shortuuidfield import ShortUUIDField


        

# Create your models here.
class Needed(models.Model):
    title = models.CharField(max_length=120, unique=True)
    body = models.TextField()
    uuid = ShortUUIDField()
    
    likes = models.IntegerField(default=0)
    liked_by = models.ManyToManyField(User, related_name="UserProfile.liked")
   
    
    posted = models.DateField(auto_now_add=True, auto_now=False)
    
    
   
    def __unicode__(self):
        return self.title

class UserProfile(models.Model):
    
    user = models.OneToOneField(User)
    website = models.URLField(blank=True)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.TextField(default=' ')
    
    def __unicode__(self):
        return self.user.username

