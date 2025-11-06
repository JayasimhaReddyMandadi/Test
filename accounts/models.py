from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver
from django.db.models.signals import post_save


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='incomes')
    source = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.source} - {self.amount}"


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    category = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.category} - {self.amount}"


class MutualFund(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mutual_funds')
    name = models.CharField(max_length=255)
    fund_type = models.CharField(max_length=50)
    invested_amount = models.DecimalField(max_digits=12, decimal_places=2)
    current_value = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.fund_type})"
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    rider_id = models.CharField(max_length=8, unique=True, null=True, blank=True, db_index=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.username} - Rider ID: {self.rider_id}'
    
    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'
        ordering = ['-created_at']

# Additional model to explicitly track rider information
class RiderInfo(models.Model):
    rider_id = models.CharField(max_length=8, unique=True, primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='rider_info')
    email = models.EmailField()  # Duplicate for quick access
    username = models.CharField(max_length=150)  # Duplicate for quick access
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'Rider {self.rider_id} - {self.email}'
    
    class Meta:
        verbose_name = 'Rider Information'
        verbose_name_plural = 'Rider Information'
        ordering = ['-created_at']

# --- SIGNAL TO AUTO-CREATE PROFILE AND RIDER INFO ---
# This function creates a Profile and RiderInfo the moment a User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        import random
        # Generate a unique 8-digit rider_id (numbers only)
        rider_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        # Ensure uniqueness across both Profile and RiderInfo
        while (Profile.objects.filter(rider_id=rider_id).exists() or 
               RiderInfo.objects.filter(rider_id=rider_id).exists()):
            rider_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        
        # Create Profile
        Profile.objects.create(user=instance, rider_id=rider_id)
        
        # Create RiderInfo for explicit tracking
        RiderInfo.objects.create(
            rider_id=rider_id,
            user=instance,
            email=instance.email,
            username=instance.username
        )

# Signal to update RiderInfo when User is updated
@receiver(post_save, sender=User)
def update_rider_info(sender, instance, created, **kwargs):
    if not created:  # Only for updates, not creation
        try:
            rider_info = instance.rider_info
            rider_info.email = instance.email
            rider_info.username = instance.username
            rider_info.save()
        except RiderInfo.DoesNotExist:
            # If RiderInfo doesn't exist, create it
            try:
                profile = instance.profile
                if profile.rider_id:
                    RiderInfo.objects.create(
                        rider_id=profile.rider_id,
                        user=instance,
                        email=instance.email,
                        username=instance.username
                    )
            except Profile.DoesNotExist:
                pass

