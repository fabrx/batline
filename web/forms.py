from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import Commentaire, Fichier, Membre, MessageContact, Post


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


class CommentaireForm(ModelForm):
    class Meta:
        model=Commentaire
        fields=["texte"]


class ContactForm(ModelForm):
    class Meta:
        model=MessageContact
        fields=["nom","email","message"]
