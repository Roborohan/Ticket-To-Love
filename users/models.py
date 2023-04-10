from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.utils import timezone
# Extending User Model Using a One-To-One Link
class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    SEXUALITY_CHOICES = (
        ('H', 'Heterosexual'),
        ('B', 'Bisexual'),
        ('G', 'Homosexual'),
        ('N', 'No preference'),
    )


    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date_of_birth = models.DateField(default=timezone.now)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    sexuality = models.CharField(max_length=1, choices=SEXUALITY_CHOICES)
    avatar = models.ImageField(default='default.jpg', upload_to='profile_images')
    bio = models.CharField(max_length=140, null=True, blank=True)

    def __str__(self):
        return self.user.username
    def __int__(self):
        return self.user.id

    # resizing images
    def save(self, *args, **kwargs):
        super().save()

        img = Image.open(self.avatar.path)

        if img.height > 100 or img.width > 100:
            new_img = (100, 100)
            img.thumbnail(new_img)
            img.save(self.avatar.path)
