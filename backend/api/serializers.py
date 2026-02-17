from rest_framework import serializers
from .models import Categorie, Annonce, ImageAnnonce
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = '__all__'

class ImageAnnonceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAnnonce
        fields = ['id', 'image', 'est_principale']

class AnnonceSerializer(serializers.ModelSerializer):
    images = ImageAnnonceSerializer(many=True, read_only=True)
    categorie_nom = serializers.CharField(source='categorie.nom', read_only=True)
    utilisateur_nom = serializers.CharField(source='utilisateur.username', read_only=True)
    
    class Meta:
        model = Annonce
        fields = [
            'id', 'titre', 'description', 'categorie', 'categorie_nom',
            'prix', 'ville', 'code_postal', 'utilisateur', 'utilisateur_nom',
            'date_creation', 'vues', 'images'
        ]
        read_only_fields = ['utilisateur', 'date_creation', 'vues']