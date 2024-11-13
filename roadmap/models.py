from django.db import models
from django.contrib.auth.models import User
import numpy as np

def genDefaultArray():
    return np.zeros(1536, dtype=np.int64).tobytes()
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_job = models.CharField(max_length=100, blank=True)
    dream_job = models.CharField(max_length=100, blank=True)
    skills = models.TextField(blank=True)
    chat_history = models.JSONField(default=list)
    

    def __str__(self):
        return self.user.username
class Intereses(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    color = models.CharField(max_length=7, default="#000000")
    def __str__(self):
        return self.name
class UserIntereses(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    interest = models.ForeignKey(Intereses, on_delete=models.CASCADE)
    def __str__(self):
        return f'{self.user} is interested in {self.interes}'
class Roadmap(models.Model):
    mainGoal = models.TextField()
    content = models.JSONField()
    completionPercentage = models.IntegerField(default=0)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    interest = models.ForeignKey(Intereses, on_delete=models.CASCADE)
    embedding = models.BinaryField(default=genDefaultArray())
    def __str__(self):
        return self.mainGoal
class Checkpoint(models.Model):
    numberOfCheckpoint = models.IntegerField(default=0)
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, default=0)
    completed = models.BooleanField()

    def __str__(self):
        return f'# Checkpoint: {self.numberOfCheckpoint} - Roadmap ID {self.roadmap}'
  
