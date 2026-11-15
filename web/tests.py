import shutil
import tempfile

from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import Branche, Categorie, Faculte, Fichier, Membre, Post, Promotion, Universite

MEDIA_TMP = tempfile.mkdtemp()


@override_settings(MEDIA_ROOT=MEDIA_TMP)
class BatlineTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(MEDIA_TMP, ignore_errors=True)

    @classmethod
    def setUpTestData(cls):
        cls.univ = Universite.objects.create(
            sigle="UNIKIN", nom="Universite de Kinshasa", adresse="Kinshasa",
            date_de_creation=1954, nombre_etudiant=30000,
        )
        cls.fac = Faculte.objects.create(nom_fac="Economie", logo="fase.JPG")
        cls.promo = Promotion.objects.create(nom_promo="G1", faculte=cls.fac)
        cls.cat = Categorie.objects.create(nom_cat="Syllabus")
        cls.branche = Branche.objects.create(nom_branche="Macroeconomie", promotion=cls.promo)
        cls.branche.branche_categorie.add(cls.cat)
        cls.fichier = Fichier.objects.create(
            titre_document="Syllabus macro", universite="UNIKIN",
            fichier=SimpleUploadedFile("macro.pdf", b"%PDF-1.4"),
            faculte=cls.fac, categorie=cls.cat, promotion=cls.promo,
        )

    # --- modeles -------------------------------------------------------------
    def test_creer_un_user_ne_plante_plus(self):
        # Avant, un signal post_save creait un Membre incomplet et levait une erreur.
        User.objects.create_superuser("admin", "admin@example.com", "motdepasse-solide")
        self.assertEqual(Membre.objects.count(), 0)

    def test_choix_promotion_sans_doublon(self):
        codes = [c for c, _ in Promotion.PROMOTION]
        self.assertEqual(len(codes), len(set(codes)))
        self.assertIn("D2", codes)

    def test_str_fichier_sans_titre(self):
        f = Fichier(fichier="doc.pdf")
        self.assertEqual(str(f), "doc.pdf")

    # --- pages publiques ----------------------------------------------------
    def test_pages_publiques(self):
        urls = [
            reverse("web:accueil"), reverse("web:faculte"), reverse("web:contact"),
            reverse("web:forum"), reverse("web:discussions"), reverse("web:login"),
            reverse("web:register"), reverse("web:hello"),
            reverse("web:promotion", args=[self.fac.pk]),
            reverse("web:branche", args=[self.promo.pk]),
            reverse("web:fichier", args=[self.cat.pk]),
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_racine_redirige_vers_accueil(self):
        self.assertRedirects(self.client.get("/"), reverse("web:accueil"))

    def test_navigation_affiche_les_donnees(self):
        self.assertContains(self.client.get(reverse("web:faculte")), "Economie")
        self.assertContains(self.client.get(reverse("web:branche", args=[self.promo.pk])), "Macroeconomie")
        self.assertContains(self.client.get(reverse("web:fichier", args=[self.cat.pk])), "Syllabus macro")

    def test_id_inexistant_renvoie_404(self):
        for name in ("web:promotion", "web:branche", "web:fichier", "web:details"):
            with self.subTest(name=name):
                self.assertEqual(self.client.get(reverse(name, args=[9999])).status_code, 404)

    # --- posts ----------------------------------------------------------------
    def test_discussions_et_detail(self):
        post = Post.objects.create(faculte=self.fac, titre="Examen", body="Date ?", fichier=self.fichier)
        self.assertContains(self.client.get(reverse("web:discussions")), "Examen")
        self.assertContains(self.client.get(reverse("web:details", args=[post.pk])), "Date ?")

    def test_publication_exige_connexion(self):
        for name in ("web:new-post", "web:new-file"):
            with self.subTest(name=name):
                resp = self.client.get(reverse(name))
                self.assertRedirects(resp, reverse("web:login") + "?next=" + reverse(name))

    def test_creer_un_post_connecte(self):
        User.objects.create_user("bob", password="motdepasse-solide")
        self.client.login(username="bob", password="motdepasse-solide")
        resp = self.client.post(reverse("web:new-post"), {
            "faculte": self.fac.pk, "titre": "Question", "body": "Bonjour", "fichier": self.fichier.pk,
        })
        post = Post.objects.get(titre="Question")
        self.assertRedirects(resp, reverse("web:details", args=[post.pk]))

    # --- inscription / connexion ---------------------------------------------
    def test_inscription_cree_un_membre_et_connecte(self):
        resp = self.client.post(reverse("web:register"), {
            "username": "alice", "first_name": "Alice", "last_name": "K",
            "age": 21, "genre": "Mlle", "universite": self.univ.pk,
            "faculte": self.fac.pk, "promotion": self.promo.pk,
            "email": "alice@example.com",
            "password1": "un-mot-de-passe-solide", "password2": "un-mot-de-passe-solide",
        })
        self.assertRedirects(resp, reverse("web:accueil"))
        membre = Membre.objects.get(username="alice")
        self.assertEqual(membre.universite, self.univ)
        self.assertTrue(membre.check_password("un-mot-de-passe-solide"))
        self.assertEqual(int(self.client.session["_auth_user_id"]), membre.pk)

    def test_connexion_puis_deconnexion(self):
        User.objects.create_user("bob", password="motdepasse-solide")
        resp = self.client.post(reverse("web:login"), {"username": "bob", "password": "motdepasse-solide"})
        self.assertRedirects(resp, reverse("web:accueil"))
        self.assertContains(self.client.get(reverse("web:accueil")), "Deconnexion")
        self.client.post(reverse("web:logout"))
        self.assertNotIn("_auth_user_id", self.client.session)
