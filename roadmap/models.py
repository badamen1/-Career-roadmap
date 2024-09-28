from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_job = models.CharField(max_length=100, blank=True)
    dream_job = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)
    chat_history = models.JSONField(default=list)
    

    def __str__(self):
        return self.user.username