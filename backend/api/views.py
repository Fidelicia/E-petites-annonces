from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Categorie, Annonce, ImageAnnonce
from .serializers import CategorieSerializer, AnnonceSerializer
from django.contrib.auth.models import User

class CategorieViewSet(viewsets.ModelViewSet):
    queryset = Categorie.objects.all()
    serializer_class = CategorieSerializer
    permission_classes = [permissions.AllowAny]

class AnnonceViewSet(viewsets.ModelViewSet):
    queryset = Annonce.objects.all().order_by('-date_creation')
    serializer_class = AnnonceSerializer
    permission_classes = [permissions.AllowAny]
    
    def perform_create(self, serializer):
        serializer.save(utilisateur=self.request.user)
    
    @action(detail=False, methods=['get'])
    def recentes(self, request):
        """Annonces récentes (5 dernières)"""
        annonces = Annonce.objects.all().order_by('-date_creation')[:5]
        serializer = self.get_serializer(annonces, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def incrementer_vues(self, request, pk=None):
        annonce = self.get_object()
        annonce.vues += 1
        annonce.save()
        return Response({'vues': annonce.vues})