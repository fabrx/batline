from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *


class PostForm(ModelForm):
    class Meta:
        model=Post
        fields=["faculte","titre","body","fichier"]

class FichierForm(ModelForm):
    class Meta:
        model=Fichier
        exclude=["id"]


class RegistrationForm(UserCreationForm):
    class Meta:
        model=Membre
        fields=(
            'username',
            'first_name',
            'last_name',
            'age',
            'genre',
            'universite',
            'faculte',
            'promotion',
            'email',
            'password1',
            'password2'
        )
    def save(self,commit=True):
        user=super(RegistrationForm,self).save(commit=False)
        user.username=self.cleaned_data['username']
        user.first_name=self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email']
        user.genre = self.cleaned_data['genre']
        user.promotion = self.cleaned_data['promotion']
        user.age = self.cleaned_data['age']

        if commit:
            user.save()
        return user
