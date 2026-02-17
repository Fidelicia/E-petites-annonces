from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid

class Categorie(models.Model):
    """Catégorie d'annonces"""
    nom = models.CharField(max_length=100)
    icon = models.CharField(max_length=50, default='📦')
    couleur = models.CharField(max_length=7, default='#06D6A0')
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom

class Annonce(models.Model):
    """Annonce principale"""
    TYPE_CHOICES = [
        ('offre', 'Offre'),
        ('demande', 'Demande'),
        ('echange', 'Échange'),
        ('location', 'Location'),
        ('don', 'Don'),
    ]
    
    STATUT_CHOICES = [
        ('brouillon', 'Brouillon'),
        ('active', 'Active'),
        ('vendu', 'Vendu'),
        ('supprime', 'Supprimé'),
        ('expire', 'Expiré'),
    ]
    
    ETAT_CHOICES = [
        ('neuf', 'Neuf'),
        ('tres_bon', 'Très bon état'),
        ('bon', 'Bon état'),
        ('moyen', 'État moyen'),
        ('a_renover', 'À rénover'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='annonces')
    titre = models.CharField(max_length=200)
    description = models.TextField()
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    categorie = models.ForeignKey(Categorie, on_delete=models.SET_NULL, null=True)
    
    # Localisation
    ville = models.CharField(max_length=100)
    code_postal = models.CharField(max_length=10)
    adresse = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    
    # Caractéristiques
    type_annonce = models.CharField(max_length=20, choices=TYPE_CHOICES, default='offre')
    etat = models.CharField(max_length=20, choices=ETAT_CHOICES, default='bon')
    negociable = models.BooleanField(default=True)
    
    # Statut et visibilité
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='active')
    promu = models.BooleanField(default=False)
    vues = models.IntegerField(default=0)
    favoris_count = models.IntegerField(default=0)
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    expire_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ville', 'statut']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.titre} - {self.prix}€"
    
    def increment_vues(self):
        """Incrémente le compteur de vues"""
        self.vues += 1
        self.save(update_fields=['vues'])

class AnnonceImage(models.Model):
    """Images pour une annonce"""
    annonce = models.ForeignKey(Annonce, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='annonces/')
    ordre = models.IntegerField(default=0)
    is_principal = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['ordre', 'created_at']
    
    def save(self, *args, **kwargs):
        if self.is_principal:
            # Désactiver les autres images principales
            AnnonceImage.objects.filter(
                annonce=self.annonce, 
                is_principal=True
            ).update(is_principal=False)
        super().save(*args, **kwargs)

class Favori(models.Model):
    """Favoris utilisateur"""
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['utilisateur', 'annonce']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.utilisateur.username} ❤️ {self.annonce.titre}"

class Message(models.Model):
    """Messagerie entre utilisateurs"""
    expediteur = models.ForeignKey(User, related_name='messages_envoyes', on_delete=models.CASCADE)
    destinataire = models.ForeignKey(User, related_name='messages_recus', on_delete=models.CASCADE)
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, null=True, blank=True)
    sujet = models.CharField(max_length=200, blank=True)
    contenu = models.TextField()
    lu = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.expediteur} → {self.destinataire}: {self.sujet[:30]}"

class Signalement(models.Model):
    """Signalement d'annonce"""
    TYPE_CHOICES = [
        ('inappropriate', 'Contenu inapproprié'),
        ('spam', 'Spam'),
        ('fraud', 'Fraude'),
        ('faux', 'Information fausse'),
        ('duplicata', 'Duplicata'),
        ('other', 'Autre'),
    ]
    
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE)
    utilisateur = models.ForeignKey(User, on_delete=models.CASCADE)
    type_signalement = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description = models.TextField()
    traite = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Signalement: {self.annonce.titre}"

class Conversation(models.Model):
    """Conversation entre deux utilisateurs"""
    participants = models.ManyToManyField(User, related_name='conversations')
    annonce = models.ForeignKey(Annonce, on_delete=models.CASCADE, null=True, blank=True)
    derniere_message = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-derniere_message']
    
    def __str__(self):
        participants = self.participants.all()
        return f"Conversation: {participants[0]} ↔ {participants[1]}"