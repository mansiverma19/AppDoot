from django.db import models
from django.contrib.auth.models import User


# Model to represent Android Apps
class App(models.Model):
    name = models.CharField(max_length=100)
    url = models.URLField(max_length=200, unique=True)  # Changed from package_name to url
    category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    points = models.IntegerField()
    logo = models.ImageField(upload_to='app_logos/')  # Added field to store the app logo

    def __str__(self):
        return self.name

# Model to represent User Apps (formerly UserTask)
class UserApps(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='screenshots/')
    points_earned = models.IntegerField(default=0)
    is_completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.app.name}"