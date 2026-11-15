from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "web"

urlpatterns = [
    path("", views.base, name="base"),
    path("salut/", views.hello, name="hello"),
    path("login/", auth_views.LoginView.as_view(template_name="web/authentification/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("register/", views.register, name="register"),
    path("new-post/", views.new_post, name="new-post"),
    path("new-file/", views.add_file, name="new-file"),
    path("discussions/", views.discussions, name="discussions"),
    path("discussion/<int:pk>/", views.details, name="details"),
    path("accueil/", views.accueil, name="accueil"),
    path("faculte/", views.faculte, name="faculte"),
    path("promotion/<int:cle>/", views.promotion, name="promotion"),
    path("branche/<int:cle>/", views.branche, name="branche"),
    path("fichier/<int:cat>/", views.fichier, name="fichier"),
    path("contact/", views.contact, name="contact"),
    path("forum/", views.discussions, name="forum"),
]
