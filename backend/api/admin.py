from django.contrib import admin
from .models import Categorie, Annonce, ImageAnnonce

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'icone')
    search_fields = ('nom',)

@admin.register(Annonce)
class AnnonceAdmin(admin.ModelAdmin):
    list_display = ('titre', 'prix', 'ville', 'date_creation', 'vues')
    list_filter = ('categorie', 'ville', 'date_creation')
    search_fields = ('titre', 'description', 'ville')
    date_hierarchy = 'date_creation'

@admin.register(ImageAnnonce)
class ImageAnnonceAdmin(admin.ModelAdmin):
    list_display = ('annonce', 'est_principale')
    list_filter = ('est_principale',)