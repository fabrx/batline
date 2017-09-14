from django.conf.urls import url
from django.contrib.auth.views import login,logout
from . import views

app_name="web"

urlpatterns=[
    url(r'^salut/$',views.hello,name="hello"),
    url(r'^login/$',login,{"template_name":"web/authentification/login.html"},name="login"),
    url(r'^new-post/$',views.new_post,name="new-post"),
    url(r'^$',views.base,name="base"),
    url(r'^register/$',views.register,name="register"),
    url(r'^discussions/$',views.discussions,name="discussions"),
    url(r'^discussion/(?P<pk>\d+)/$',views.details,name="details"),
    url(r'^accueil/$',views.accueil,name="accueil"),
    url(r'^promotion/(?P<cle>[0-9]+)/$',views.promotion,name="promotion"),
    url(r'^faculte/$',views.faculte,name="faculte"),
    url(r'^fichier/(?P<cat>[0-9]+)/$',views.fichier,name="fichier"),
    url(r'^branche/(?P<cle>[0-9]+)/$',views.branche,name="branche"),
    url(r'^contact/$',views.contact,name="contact")

]
