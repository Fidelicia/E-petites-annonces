# backend/annonces/serializers.py
from rest_framework import serializers
from .models import Annonce, AnnonceImage, Favori, Message, Signalement, Categorie

class AnnonceImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnonceImage
        fields = ['id', 'image', 'ordre']

class AnnonceSerializer(serializers.ModelSerializer):
    images = AnnonceImageSerializer(many=True, read_only=True)
    favori_count = serializers.IntegerField(read_only=True)
    est_favori = serializers.SerializerMethodField()
    utilisateur_nom = serializers.CharField(source='utilisateur.username', read_only=True)
    
    class Meta:
        model = Annonce
        fields = '__all__'
    
    def get_est_favori(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Favori.objects.filter(utilisateur=user, annonce=obj).exists()
        return False

class MessageSerializer(serializers.ModelSerializer):
    expediteur_nom = serializers.CharField(source='expediteur.username', read_only=True)
    
    class Meta:
        model = Message
        fields = '__all__'

# backend/annonces/views.py
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Annonce, Favori, Message, Signalement
from .serializers import AnnonceSerializer, MessageSerializer

class AnnonceViewSet(viewsets.ModelViewSet):
    queryset = Annonce.objects.filter(statut='actif').order_by('-created_at')
    serializer_class = AnnonceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categorie', 'ville', 'prix']
    search_fields = ['titre', 'description', 'ville']
    
    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

class FavoriViewSet(viewsets.ModelViewSet):
    serializer_class = AnnonceSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        favoris = Favori.objects.filter(utilisateur=self.request.user)
        return Annonce.objects.filter(id__in=favoris.values_list('annonce_id', flat=True))

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Message.objects.filter(
            destinataire=self.request.user
        ).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(expediteur=self.request.user)