from django.core.management.base import BaseCommand
from accounts.models import Profile
import random


class Command(BaseCommand):
    help = 'Update existing rider_ids to 8-digit format'

    def handle(self, *args, **options):
        profiles = Profile.objects.all()
        updated_count = 0
        
        for profile in profiles:
            if not profile.rider_id or len(profile.rider_id) != 8 or not profile.rider_id.isdigit():
                # Generate new 8-digit rider_id
                new_rider_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
                
                # Ensure uniqueness
                while Profile.objects.filter(rider_id=new_rider_id).exists():
                    new_rider_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
                
                old_rider_id = profile.rider_id
                profile.rider_id = new_rider_id
                profile.save()
                
                self.stdout.write(
                    self.style.SUCCESS(
                        f'Updated rider_id for user {profile.user.username}: {old_rider_id} -> {new_rider_id}'
                    )
                )
                updated_count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} rider_ids')
        )