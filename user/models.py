from django.db import models
from django.contrib.auth.models import User

# Optional: Profile model if you want to extend the User model with additional fields
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username