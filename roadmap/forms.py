from django import forms
from .models import UserProfile, Intereses

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['current_job', 'dream_job', 'skills']
class RoadmapCharacteristics(forms.Form):
    interest = forms.ModelChoiceField(queryset=Intereses.objects.all())
    objective = forms.CharField(max_length=255)
    salary = forms.DecimalField(max_digits=10, decimal_places=2)