from django.db import models
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
import uuid

Utilisateur = get_user_model()


# ─────────────────────────────
# DEVISE
# ─────────────────────────────
class Devise(models.Model):
    code = models.CharField(_('code'), max_length=10, unique=True)
    symbole = models.CharField(_('symbole'), max_length=5)
    nom = models.CharField(_('nom'), max_length=50)
    taux_vers_eur = models.FloatField(_('taux vers EUR'), default=1.0)
    actif = models.BooleanField(_('actif'), default=True)

    class Meta:
        verbose_name = _('Devise')
        verbose_name_plural = _('Devises')
        ordering = ['code']

    def __str__(self):
        return f"{self.nom} ({self.symbole})"


# ─────────────────────────────
# CATEGORIE
# ─────────────────────────────
class Categorie(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(_('nom'), max_length=100)
    slug = models.SlugField(_('slug'), unique=True)
    icone = models.CharField(_('icône'), max_length=50, default='mdi-tag')
    description = models.TextField(_('description'), blank=True)
    couleur = models.CharField(_('couleur'), max_length=7, default='#06D6A0')
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='sous_categories'
    )
    ordre = models.IntegerField(_('ordre'), default=0)

    class Meta:
        verbose_name = _('Catégorie')
        verbose_name_plural = _('Catégories')
        ordering = ['ordre', 'nom']

    def __str__(self):
        return self.nom


# ─────────────────────────────
# ANNONCE
# ─────────────────────────────
class Annonce(models.Model):

    STATUT_CHOICES = [
        ('brouillon', _('Brouillon')),
        ('en_attente', _('En attente')),
        ('active', _('Active')),
        ('vendu', _('Vendu')),
        ('expiree', _('Expirée')),
        ('rejetee', _('Rejetée')),
        ('archivee', _('Archivée')),
    ]

    TYPE_ANNONCE = [
        ('offre', _('Offre')),
        ('demande', _('Demande')),
        ('echange', _('Échange')),
        ('location', _('Location')),
        ('don', _('Don')),
    ]

    ETAT_CHOICES = [
        ('neuf', _('Neuf')),
        ('tres_bon', _('Très bon')),
        ('bon', _('Bon')),
        ('moyen', _('Moyen')),
        ('a_renover', _('À rénover')),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='annonces'
    )

    titre = models.CharField(_('titre'), max_length=200)
    slug = models.SlugField(_('slug'), max_length=250, unique=True, blank=True)
    description = models.TextField(_('description'))

    categorie = models.ForeignKey(
        Categorie,
        on_delete=models.PROTECT,
        related_name='annonces'
    )

    prix = models.DecimalField(_('prix'), max_digits=15, decimal_places=2)

    devise = models.ForeignKey(
        Devise,
        on_delete=models.PROTECT,
        related_name='annonces',
        null=True,
        blank=True
    )

    prix_negociable = models.BooleanField(_('prix négociable'), default=True)

    ville = models.CharField(_('ville'), max_length=100)
    code_postal = models.CharField(_('code postal'), max_length=10)
    adresse = models.CharField(_('adresse'), max_length=255, blank=True)

    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    statut = models.CharField(
        _('statut'),
        max_length=20,
        choices=STATUT_CHOICES,
        default='en_attente'
    )

    type_annonce = models.CharField(
        _('type'),
        max_length=20,
        choices=TYPE_ANNONCE,
        default='offre'
    )

    etat = models.CharField(
        _('état'),
        max_length=20,
        choices=ETAT_CHOICES,
        default='bon'
    )

    vues = models.PositiveIntegerField(default=0)
    favoris_count = models.PositiveIntegerField(default=0)

    est_promue = models.BooleanField(default=False)

    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    date_expiration = models.DateTimeField(null=True, blank=True)
    date_publication = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = _('Annonce')
        verbose_name_plural = _('Annonces')
        ordering = ['-date_creation']

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.titre)
            slug = base_slug
            counter = 1
            while Annonce.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        super().save(*args, **kwargs)


# ─────────────────────────────
# IMAGE ANNONCE
# ─────────────────────────────
class ImageAnnonce(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    annonce = models.ForeignKey(
        Annonce,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='annonces/')
    est_principale = models.BooleanField(default=False)
    ordre = models.IntegerField(default=0)

    class Meta:
        ordering = ['ordre']

    def __str__(self):
        return f"Image - {self.annonce.titre}"


# ─────────────────────────────
# FAVORI
# ─────────────────────────────
class Favori(models.Model):
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE,
        related_name='favoris'
    )
    annonce = models.ForeignKey(
        Annonce,
        on_delete=models.CASCADE,
        related_name='favoris'
    )
    date_ajout = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('utilisateur', 'annonce')

    def __str__(self):
        return f"{self.utilisateur} ❤️ {self.annonce}"


# ─────────────────────────────
# SIGNALEMENT
# ─────────────────────────────
class Signalement(models.Model):
    TYPE_SIGNALEMENT = [
        ('inapproprie', _('Contenu inapproprié')),
        ('arnaque', _('Arnaque')),
        ('faux', _('Information fausse')),
        ('duplicata', _('Duplicata')),
        ('autre', _('Autre')),
    ]

    annonce = models.ForeignKey(
        Annonce,
        on_delete=models.CASCADE,
        related_name='signalements'
    )
    utilisateur = models.ForeignKey(
        Utilisateur,
        on_delete=models.CASCADE
    )
    type_signalement = models.CharField(
        max_length=20,
        choices=TYPE_SIGNALEMENT
    )
    description = models.TextField()
    date_signalement = models.DateTimeField(auto_now_add=True)
    traite = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.type_signalement} - {self.annonce}"
