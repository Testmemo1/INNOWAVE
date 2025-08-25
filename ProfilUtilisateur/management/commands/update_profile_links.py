from django.core.management.base import BaseCommand
from ProfilUtilisateur.models import Utilisateur
from django.conf import settings

class Command(BaseCommand):
    help = 'Update Utilisateur.profile_link based on settings.SITE_BASE_URL'

    def handle(self, *args, **options):
        base_url = getattr(settings, 'SITE_BASE_URL', None)
        if not base_url:
            self.stdout.write(self.style.ERROR('SITE_BASE_URL is not set in settings. Aborting.'))
            return

        users = Utilisateur.objects.all()
        count = 0
        for u in users:
            u.profile_link = f"{base_url}/profiles/{u.slug}"
            u.save()
            count += 1
        self.stdout.write(self.style.SUCCESS(f'Updated profile_link for {count} users.'))
