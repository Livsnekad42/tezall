from django.db import models
from django.contrib.auth import get_user_model

from core.models import TimestampedModel


User = get_user_model()


class Profile(TimestampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    region = models.TextField(max_length=250, blank=True)
    city = models.TextField(max_length=250, blank=True)
    phone = models.CharField(max_length=15, unique=True, blank=True, null=True)
    date_birth = models.DateField("Дата Рождения", blank=True, null=True)
    failed_attempt = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        try:
            this = Profile.objects.get(id=self.id)
            
        except Profile.DoesNotExist:
            this = None
        
        super(Profile, self).save(*args, **kwargs)
    
    def get_full_name(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    def get_short_name(self):
        return f"{self.user.last_name} {self.user.first_name[0]}."
