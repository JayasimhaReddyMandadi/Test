from django.core.management.base import BaseCommand
from accounts.models import Profile, RiderInfo
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = 'Populate RiderInfo table for existing users'

    def handle(self, *args, **options):
        created_count = 0
        updated_count = 0
        
        # Get all profiles with rider_id
        profiles = Profile.objects.filter(rider_id__isnull=False).select_related('user')
        
        for profile in profiles:
            user = profile.user
            rider_id = profile.rider_id
            
            # Check if RiderInfo already exists
            rider_info, created = RiderInfo.objects.get_or_create(
                rider_id=rider_id,
                defaults={
                    'user': user,
                    'email': user.email,
                    'username': user.username,
                    'is_active': True
                }
            )
            
            if created:
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Created RiderInfo for {user.username} (Rider ID: {rider_id})'
                    )
                )
                created_count += 1
            else:
                # Update existing RiderInfo if needed
                updated = False
                if rider_info.email != user.email:
                    rider_info.email = user.email
                    updated = True
                if rider_info.username != user.username:
                    rider_info.username = user.username
                    updated = True
                
                if updated:
                    rider_info.save()
                    self.stdout.write(
                        self.style.WARNING(
                            f'Updated RiderInfo for {user.username} (Rider ID: {rider_id})'
                        )
                    )
                    updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Successfully processed RiderInfo: {created_count} created, {updated_count} updated'
            )
        )