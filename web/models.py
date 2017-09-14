from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.




class Faculte(models.Model):
    nom_fac=models.CharField(max_length=30)
    logo=models.ImageField()

    def __str__(self):
        return self.nom_fac


class Promotion(models.Model):
	PROMOTION=(
        ("G0","Preparatoire"),
        ("G1","1er Graduat"),
        ("G2","2eme Graduat"),
        ("G3","3eme Graduat"),
        ("L1","1er Licence"),
        ("L2","2eme Licence"),
        ("D1","1er Doctorat"),
        ("D1","1er Doctorat"),
        ("D3","3eme Doctorat"),
    )
	nom_promo=models.CharField(max_length=10,choices=PROMOTION)
	faculte=models.ForeignKey(Faculte,on_delete=models.CASCADE)

	def __str__(self):
		return "%s %s"%(self.nom_promo,self.faculte.nom_fac)


class Branche(models.Model):
	nom_branche=models.CharField(max_length=50)
	promotion=models.ForeignKey(Promotion,on_delete=models.CASCADE)
	# branche_categorie=models.ManyToMany("Categorie",through="Possede")
	branche_categorie=models.ManyToManyField("Categorie")

	def __str__(self):
		return "%s %s %s"%(self.nom_branche,self.promotion.nom_promo,self.promotion.faculte.nom_fac)



class Categorie(models.Model):
    TYPE=(
        ("Syllabus","Syllabus"),
        ("TP","Travail Pratique"),
        ("memoire","Mémoire"),
        ("tfc","TFC"),
        ("bats","BATS"),)
    nom_cat=models.CharField(max_length=12,choices=TYPE)

    def __str__(self):
        return self.nom_cat

class Universite(models.Model):
    sigle=models.CharField(max_length=10)
    nom=models.CharField(max_length=100)
    adresse=models.TextField()
    date_de_creation=models.PositiveSmallIntegerField()
    nombre_etudiant=models.PositiveIntegerField()
    nom_recteur=models.CharField(max_length=50 ,null=True, blank=True)
    def __str__(self):
        return self.sigle



#L'agent qui va soigner et envoyer les donnees
class Membre(User):
	GENRE=(
	("Mr","Monsier"),
	("Mlle","Mademoiselle"),
	("Mme","Madame")
	)
	age=models.IntegerField()
	genre=models.CharField(max_length=20,choices=GENRE)
	universite=models.ForeignKey(Universite,on_delete=models.CASCADE)
	faculte=models.ForeignKey(Faculte,on_delete=models.CASCADE)
	promotion=models.ForeignKey(Promotion,on_delete=models.CASCADE)
	user=models.OneToOneField(User,on_delete=models.CASCADE)

	def __str__(self):
		return "%s %s"%(self.first_name,self.last_name)

# @receiver(post_save,sender=User)
def create_user_profil(sender,**kwargs):
    if kwargs['created']:
        Membre.objects.create(user=kwargs['instance'])

# @receiver(post_save,sender=User)
post_save.connect(create_user_profil,sender=User)

class Fichier(models.Model):
    TITRE=(("Prof","Professeur"),("CT","Chef de travaux"),("Ass","Assistant"))
    titre_document=models.CharField(max_length=25,verbose_name="Titre de document",null=True,blank=True)
    nom_auteur=models.CharField(max_length=30,verbose_name="Nom de l'auteur", null=True,blank=True)
    titre_auteur=models.CharField(max_length=30, choices=TITRE, verbose_name="Titre e l'auteur", null=True, blank=True)
    universite=models.CharField(max_length=40)
    date_pub=models.DateTimeField(auto_now=False,auto_now_add=True)
    date_modif=models.DateTimeField(auto_now=True,auto_now_add=False)
    fichier=models.FileField()
    faculte=models.ForeignKey(Faculte,on_delete=models.CASCADE)
    categorie=models.ForeignKey(Categorie,on_delete=models.CASCADE)
    promotion=models.ForeignKey(Promotion,on_delete=models.CASCADE)

    def __str__(self):
        return self.titre_document


class Post(models.Model):
    faculte=models.ForeignKey(Faculte,on_delete=models.CASCADE)
    titre=models.CharField(max_length=50)
    body=models.TextField(blank=False)
    #fichier_post=models.FileField(null=True)
    date_pub=models.DateTimeField(auto_now_add=True,auto_now=False,verbose_name="Ajoute le")
    date_modif=models.DateTimeField(auto_now_add=False,auto_now=True)
    fichier=models.ForeignKey(Fichier,on_delete=models.CASCADE)


    def __str__(self):
        return self.titre
