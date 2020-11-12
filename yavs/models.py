from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Check entities.txt

#class User
class Video(models.Model):
    # After migration, each variable becomes a column in SQL database
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    sentiment = models.CharField(max_length=36, null=True) # Not to be filled by user! Default filled to please wait, sentiment score still processing... Until calculation is complete
    path = models.CharField(max_length=64)
    born_on = models.DateTimeField(auto_now=True, blank=False, null=False)
    uploaded_by = models.ForeignKey('auth.User', on_delete=models.CASCADE) # Deletes related entries on user deletion

class Comment(models.Model):
    text = models.CharField(max_length=500)
    born_on = models.DateTimeField(auto_now=True, blank=False, null=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)