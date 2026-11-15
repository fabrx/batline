from django.contrib import admin

from .models import (Branche, Categorie, Commentaire, Faculte, Fichier, Membre,
                     MessageContact, Post, Promotion, Universite)

admin.site.register(Faculte)
admin.site.register(Promotion)
admin.site.register(Branche)
admin.site.register(Categorie)
admin.site.register(Fichier)
admin.site.register(Universite)
admin.site.register(Membre)


class CommentaireInline(admin.TabularInline):
    model = Commentaire
    extra = 0


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("titre", "faculte", "auteur", "date_pub")
    list_filter = ("faculte",)
    search_fields = ("titre", "body")
    inlines = [CommentaireInline]


@admin.register(MessageContact)
class MessageContactAdmin(admin.ModelAdmin):
    list_display = ("nom", "email", "date_envoi", "lu")
    list_filter = ("lu",)
    list_editable = ("lu",)
    search_fields = ("nom", "email", "message")
    readonly_fields = ("nom", "email", "message", "date_envoi")
