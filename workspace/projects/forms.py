from django import forms
from projects.models import Needed, UserProfile
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
import re
punctuation = ('/', '-', '_', '?', '!','$','@','&', '*', '(', ')', '{', '}', '[', ']', '=',':',';',',','.','<','>', '~')
class NeededForm(forms.ModelForm):
    title = forms.CharField(max_length=120)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    body = forms.CharField(min_length=50,widget = forms.Textarea)
    captcha = CaptchaField()
    
   
    class Meta:
        model = Needed
        fields = ('title', 'body', 'likes')
        
    def clean_title(self):
        data = self.cleaned_data['title']
        for pun in punctuation:
            if pun in data:
                raise forms.ValidationError('Please remove all punctuation')    
        return data
    
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password')
        
class UserProfileForm(forms.ModelForm):
    bio = forms.CharField(widget=forms.Textarea, required=False)
    class Meta:
        model = UserProfile
        fields = ('website','bio')

