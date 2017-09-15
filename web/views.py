from django.shortcuts import render
from django.http import Http404,HttpResponse
from .forms import *
from .models import *

# Create your views here.

def hello(request):
    return render(request,"web/salut.html")

def new_post(request):
    if not request.user.is_authenticated():
        return render(request, 'web/authentification/login.html')
    else:
        if request.method=="GET":
            form=PostForm()
            context={
                "form":form
            }
            return render(request,"web/ajouter_post.html",context)
        elif request.method=="POST":
            form=PostForm(request.POST or None,request.FILES or None)
            if form.is_valid():
                post=form.save(commit=False)
                post.save()
            else:
                print("Erreur")


#Ici sera la liste de tous les postes
def discussions(request):
    post=Post.objects.all().order_by('-date_pub')[:5]
    context={
        "post":post
    }
    return render(request,"web/list_posts.html",post)
#Details sur un poste particulier
def details(request,pk):
    instance=get_object_or_404(Post,id=pk)
    context={
        "details":details
    }
    return render(request,"web/list_posts_details.html",context)

def addFile(request):
    if not request.user.is_authenticated():
        return render(request, 'web/authentification/login.html')
    if request.method=="POST":
        form=FichierForm(request.POST or None,request.FILES or None)
        if form.is_valid():
            form.save()
    elif request.method=="GET":
        form=FichierForm()
        context={"form":form}
        return render(request,"web/ajouter_fichier.html",context)


def register(request):
    if request.user.is_authenticated():
        pass
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("web:home")
    else:
        form=RegistrationForm()
        args={"form":form}
        return render(request,"web/authentification/register.html",args)

def base(request):
    # if not request.user.is_authenticated():
    #     return render(request, 'web/authentification/login.html')
    return render(request,"web/base.html")

def accueil(request):
    return render(request,"web/accueil.html")


def faculte(request):
    fac=Faculte.objects.all()
    return render(request,"web/faculte.html",{"f":fac})

def promotion(request,cle):
    fac=Faculte.objects.get(id=cle)
    promo=Promotion.objects.filter(faculte=fac)
    return render(request,"web/promotion.html",{"p":promo})

def branche(request,cle):
    promo=Promotion.objects.get(id=cle)
    brch=Branche.objects.filter(promotion=promo)
    return render(request,"web/branche.html", {"b":brch})



def fichier(request,cat):
    cat=Categorie.objects.get(id=cat)
    fich=Fichier.objects.filter(categorie=cat)
    return render(request,"web/fichier.html",{"f":fich})

def contact(request):
    return render(request,"web/contact.html")

def forum(request,cle):
    #forum=Forum.objects.all()
    return render(request,"web/forum.html",)

def commentaire(request):
    return render(request,"web/commentaire.html")
