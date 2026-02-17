from rest_framework import viewsets, permissions, status, generics
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q, Count
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

from .models import Annonce, Favori, Message, Signalement, Conversation, AnnonceImage, Categorie
from .serializers import (
    AnnonceSerializer, FavoriSerializer, MessageSerializer,
    SignalementSerializer, ConversationSerializer, AnnonceCreateSerializer,
    AnnonceImageSerializer, CategorieSerializer
)
from .filters import AnnonceFilter
from .permissions import IsOwnerOrReadOnly, IsMessageParticipant

class CategorieViewSet(viewsets.ReadOnlyModelViewSet):
    """Catégories d'annonces"""
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [permissions.AllowAny]

class AnnonceViewSet(viewsets.ModelViewSet):
    """Gestion des annonces"""
    queryset = Annonce.objects.filter(statut='active').select_related(
        'utilisateur', 'categorie'
    ).prefetch_related('images')
    
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = AnnonceFilter
    search_fields = ['titre', 'description', 'ville']
    ordering_fields = ['prix', 'created_at', 'vues', 'favoris_count']
    ordering = ['-created_at']
    
    def get_permissions(self):
        """Permissions différenciées"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]
    
    def get_serializer_class(self):
        """Serializer différent pour création/mise à jour"""
        if self.action in ['create', 'update', 'partial_update']:
            return AnnonceCreateSerializer
        return AnnonceSerializer
    
    def perform_create(self, serializer):
        """Création avec utilisateur courant"""
        serializer.save(utilisateur=self.request.user)
    
    @action(detail=True, methods=['post'])
    def increment_vues(self, request, pk=None):
        """Incrémente les vues d'une annonce"""
        annonce = self.get_object()
        annonce.increment_vues()
        return Response({'vues': annonce.vues})
    
    @action(detail=True, methods=['get'])
    def similaires(self, request, pk=None):
        """Annonces similaires"""
        annonce = self.get_object()
        similaires = Annonce.objects.filter(
            categorie=annonce.categorie,
            ville=annonce.ville,
            statut='active'
        ).exclude(id=annonce.id)[:6]
        serializer = self.get_serializer(similaires, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def geolocalisees(self, request):
        """Annonces géolocalisées près d'un point"""
        lat = request.query_params.get('lat')
        lng = request.query_params.get('lng')
        radius = request.query_params.get('radius', 10)  # km
        
        if lat and lng:
            point = Point(float(lng), float(lat))
            annonces = Annonce.objects.filter(
                latitude__isnull=False,
                longitude__isnull=False,
                statut='active'
            ).annotate(
                distance=Distance('position', point)
            ).filter(distance__lte=Distance(km=radius)).order_by('distance')
            
            serializer = self.get_serializer(annonces, many=True)
            return Response(serializer.data)
        
        return Response([])

class FavoriViewSet(viewsets.ModelViewSet):
    """Gestion des favoris"""
    serializer_class = FavoriSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Favori.objects.filter(utilisateur=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)
    
    @action(detail=False, methods=['get'])
    def annonces(self, request):
        """Liste des annonces favorites"""
        favoris = self.get_queryset().select_related('annonce')
        annonces = [f.annonce for f in favoris]
        serializer = AnnonceSerializer(annonces, many=True, context={'request': request})
        return Response(serializer.data)

class MessageViewSet(viewsets.ModelViewSet):
    """Messagerie"""
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, IsMessageParticipant]
    
    def get_queryset(self):
        user = self.request.user
        return Message.objects.filter(
            Q(expediteur=user) | Q(destinataire=user)
        ).order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(expediteur=self.request.user)
    
    @action(detail=False, methods=['get'])
    def conversations(self, request):
        """Liste des conversations"""
        user = request.user
        messages = Message.objects.filter(
            Q(expediteur=user) | Q(destinataire=user)
        ).order_by('annonce', '-created_at')
        
        conversations = {}
        for message in messages:
            annonce_id = message.annonce_id if message.annonce else 0
            other_user = message.destinataire if message.expediteur == user else message.expediteur
            
            key = f"{annonce_id}_{other_user.id}"
            if key not in conversations:
                conversations[key] = {
                    'annonce': message.annonce,
                    'other_user': other_user,
                    'last_message': message,
                    'unread_count': Message.objects.filter(
                        destinataire=user,
                        expediteur=other_user,
                        lu=False
                    ).count()
                }
        
        return Response(list(conversations.values()))

class SignalementViewSet(viewsets.ModelViewSet):
    """Signalements"""
    serializer_class = SignalementSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Signalement.objects.filter(utilisateur=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)

class AnnonceImageCreateView(generics.CreateAPIView):
    """Upload d'images pour annonces"""
    serializer_class = AnnonceImageSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def perform_create(self, serializer):
        annonce_id = self.request.data.get('annonce')
        annonce = get_object_or_404(Annonce, id=annonce_id, utilisateur=self.request.user)
        serializer.save(annonce=annonce)