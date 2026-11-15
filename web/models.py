from django.db import models
from django.contrib.auth.models import User

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
        ("D2","2eme Doctorat"),
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
	("Mr","Monsieur"),
	("Mlle","Mademoiselle"),
	("Mme","Madame")
	)
	age=models.IntegerField()
	genre=models.CharField(max_length=20,choices=GENRE)
	universite=models.ForeignKey(Universite,on_delete=models.CASCADE)
	faculte=models.ForeignKey(Faculte,on_delete=models.CASCADE)
	promotion=models.ForeignKey(Promotion,on_delete=models.CASCADE)
	# Lien vers l'utilisateur parent (heritage multi-table). Il correspond a la
	# colonne "user_id" deja presente dans la base.
	user=models.OneToOneField(User,on_delete=models.CASCADE,parent_link=True,primary_key=True)

	def __str__(self):
		return "%s %s"%(self.first_name,self.last_name)

# Note : un signal post_save creait automatiquement un Membre pour chaque User,
# mais Membre exige age/genre/universite/... : toute creation d'utilisateur
# (createsuperuser compris) plantait. Le Membre est desormais cree par le
# formulaire d'inscription (RegistrationForm).

class Fichier(models.Model):
    TITRE=(("Prof","Professeur"),("CT","Chef de travaux"),("Ass","Assistant"))
    titre_document=models.CharField(max_length=25,verbose_name="Titre de document",null=True,blank=True)
    nom_auteur=models.CharField(max_length=30,verbose_name="Nom de l'auteur", null=True,blank=True)
    titre_auteur=models.CharField(max_length=30, choices=TITRE, verbose_name="Titre de l'auteur", null=True, blank=True)
    universite=models.CharField(max_length=40)
    date_pub=models.DateTimeField(auto_now=False,auto_now_add=True)
    date_modif=models.DateTimeField(auto_now=True,auto_now_add=False)
    fichier=models.FileField()
    faculte=models.ForeignKey(Faculte,on_delete=models.CASCADE)
    categorie=models.ForeignKey(Categorie,on_delete=models.CASCADE)
    promotion=models.ForeignKey(Promotion,on_delete=models.CASCADE)

    def __str__(self):
        return self.titre_document or self.fichier.name


class Post(models.Model):
    faculte=models.ForeignKey(Faculte,on_delete=models.CASCADE)
    titre=models.CharField(max_length=50)
    body=models.TextField(blank=False)
    #fichier_post=models.FileField(null=True)
    date_pub=models.DateTimeField(auto_now_add=True,auto_now=False,verbose_name="Ajoute le")
    date_modif=models.DateTimeField(auto_now_add=False,auto_now=True)
    fichier=models.ForeignKey(Fichier,on_delete=models.SET_NULL,null=True,blank=True,verbose_name="Fichier joint")
    auteur=models.ForeignKey(User,on_delete=models.SET_NULL,null=True,blank=True)

    def __str__(self):
        return self.titre


class Commentaire(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="commentaires")
    auteur=models.ForeignKey(User,on_delete=models.CASCADE)
    texte=models.TextField(verbose_name="Commentaire")
    date_pub=models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering=["date_pub"]

    def __str__(self):
        return "%s sur %s"%(self.auteur,self.post)


class MessageContact(models.Model):
    nom=models.CharField(max_length=50,verbose_name="Prenom")
    email=models.EmailField(verbose_name="E-mail")
    message=models.TextField()
    date_envoi=models.DateTimeField(auto_now_add=True)
    lu=models.BooleanField(default=False)

    class Meta:
        ordering=["-date_envoi"]
        verbose_name="message de contact"
        verbose_name_plural="messages de contact"

    def __str__(self):
        return "%s <%s>"%(self.nom,self.email)
