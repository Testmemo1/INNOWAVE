from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.text import slugify
from django.conf import settings

class Utilisateur(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='cover_images/', blank=True, null=True)
    date_naissance = models.DateField(blank=True, null=True)
    adresse = models.CharField(max_length=255, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    genre = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')], blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    profile_link = models.URLField(blank=True, null=True)

    # Champ JSON pour stocker plusieurs comptes de réseaux sociaux
    reseaux_sociaux = models.JSONField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.username)
        # Utilisation du domaine dynamique selon l'environnement.
        # IMPORTANT: do not default to localhost here to avoid storing 127.0.0.1 in production.
        base_url = getattr(settings, 'SITE_BASE_URL', None)
        if base_url:
            self.profile_link = f"{base_url}/profiles/{self.slug}"
        else:
            # Clear or leave empty when SITE_BASE_URL is not configured.
            self.profile_link = ''
        super().save(*args, **kwargs)

    @property
    def absolute_profile_link(self):
        """Return an absolute profile URL using SITE_BASE_URL when available, else None.

        Use this property when you need a fully qualified URL (emails, admin links).
        """
        base_url = getattr(settings, 'SITE_BASE_URL', None)
        if base_url:
            return f"{base_url}/profiles/{self.slug}"
        return None

    def get_absolute_url(self):
        """Return the relative URL for this user's profile.

        Use this in templates or admin to avoid storing absolute localhost links.
        """
        return f"/profiles/{self.slug}"

    def __str__(self):
        return self.username


class HistoriqueConnexion(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    adresse_ip = models.GenericIPAddressField()

    def __str__(self):
        return f"Connexion de {self.utilisateur.username} le {self.date}"
