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
    rider_id = models.CharField(max_length=8, unique=True, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'

# --- SIGNAL TO AUTO-CREATE PROFILE ---
# This function creates a Profile the moment a User is created.
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        import random
        # Generate a unique 8-digit rider_id (numbers only)
        rider_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        # Ensure uniqueness
        while Profile.objects.filter(rider_id=rider_id).exists():
            rider_id = ''.join([str(random.randint(0, 9)) for _ in range(8)])
        
        Profile.objects.create(user=instance, rider_id=rider_id)

