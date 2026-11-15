from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FichierForm, PostForm, RegistrationForm
from .models import Branche, Categorie, Faculte, Fichier, Post, Promotion


def hello(request):
    return render(request, "web/salut.html")


def base(request):
    return render(request, "web/base.html")


def accueil(request):
    return render(request, "web/accueil.html")


def contact(request):
    return render(request, "web/contact.html")


def forum(request):
    return render(request, "web/forum.html")


def commentaire(request):
    return render(request, "web/commentaire.html")


@login_required
def new_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        post = form.save()
        return redirect("web:details", pk=post.pk)
    return render(request, "web/ajouter_post.html", {"form": form})


def discussions(request):
    """Les 5 derniers posts."""
    posts = Post.objects.select_related("faculte").order_by("-date_pub")[:5]
    return render(request, "web/list_posts.html", {"posts": posts})


def details(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "web/list_posts_details.html", {"post": post})


@login_required
def add_file(request):
    form = FichierForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        fichier = form.save()
        return redirect("web:fichier", cat=fichier.categorie_id)
    return render(request, "web/ajouter_post.html", {"form": form})


def register(request):
    if request.user.is_authenticated:
        return redirect("web:accueil")
    form = RegistrationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("web:accueil")
    return render(request, "web/authentification/register.html", {"form": form})


def faculte(request):
    return render(request, "web/faculte.html", {"f": Faculte.objects.all()})


def promotion(request, cle):
    fac = get_object_or_404(Faculte, pk=cle)
    return render(request, "web/promotion.html", {"p": fac.promotion_set.all()})


def branche(request, cle):
    promo = get_object_or_404(Promotion, pk=cle)
    brch = Branche.objects.filter(promotion=promo).prefetch_related("branche_categorie")
    return render(request, "web/branche.html", {"b": brch})


def fichier(request, cat):
    categorie = get_object_or_404(Categorie, pk=cat)
    fich = Fichier.objects.filter(categorie=categorie).order_by("-date_pub")
    return render(request, "web/fichier.html", {"f": fich})
