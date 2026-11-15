from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .forms import CommentaireForm, ContactForm, FichierForm, PostForm, RegistrationForm
from .models import Branche, Categorie, Faculte, Fichier, Post, Promotion


def hello(request):
    return render(request, "web/salut.html")


def base(request):
    return render(request, "web/base.html")


def accueil(request):
    return render(request, "web/accueil.html")


def derniers_posts(nombre=5):
    return (Post.objects.select_related("auteur", "faculte")
            .annotate(nb_commentaires=Count("commentaires"))
            .order_by("-date_pub")[:nombre])


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Merci ! Votre message a bien ete envoye.")
        return redirect("web:contact")
    return render(request, "web/contact.html", {"form": form})


@login_required
def new_post(request):
    form = PostForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        post = form.save(commit=False)
        post.auteur = request.user
        post.save()
        messages.success(request, "Votre discussion a ete publiee.")
        return redirect("web:details", pk=post.pk)
    return render(request, "web/ajouter_post.html", {"form": form})


def discussions(request):
    """Forum : toutes les discussions, 10 par page."""
    posts = (Post.objects.select_related("auteur", "faculte")
             .annotate(nb_commentaires=Count("commentaires"))
             .order_by("-date_pub"))
    page = Paginator(posts, 10).get_page(request.GET.get("page"))
    return render(request, "web/list_posts.html", {"page": page, "posts": page.object_list})


def details(request, pk):
    post = get_object_or_404(Post.objects.select_related("auteur", "faculte", "fichier"), pk=pk)
    form = CommentaireForm(request.POST or None)
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("%s?next=%s" % (reverse("web:login"), request.path))
        if form.is_valid():
            com = form.save(commit=False)
            com.post = post
            com.auteur = request.user
            com.save()
            return redirect(reverse("web:details", args=[post.pk]) + "#commentaires")
    commentaires = post.commentaires.select_related("auteur")
    return render(request, "web/list_posts_details.html",
                  {"post": post, "commentaires": commentaires, "form": form})


@login_required
def add_file(request):
    form = FichierForm(request.POST or None, request.FILES or None)
    if request.method == "POST" and form.is_valid():
        fichier = form.save()
        messages.success(request, "Fichier publie.")
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
    return render(request, "web/faculte.html",
                  {"f": Faculte.objects.all(), "derniers_posts": derniers_posts()})


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
