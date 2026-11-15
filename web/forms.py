from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Fichier, Membre, Post


class PostForm(ModelForm):
    class Meta:
        model=Post
        fields=["faculte","titre","body","fichier"]

class FichierForm(ModelForm):
    class Meta:
        model=Fichier
        exclude=["date_pub","date_modif"]


class RegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
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
        )
