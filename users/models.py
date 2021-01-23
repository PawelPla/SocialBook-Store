from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(default=1, null=True, blank=True)
    profile_pic = models.ImageField(upload_to='profile_pics', blank=True, null=True, name='profile_pic')

    def __str__(self):
        return self.username

    def num_reviews(self):
        revs = CustomUser.objects.filter(username=self).first().reviews.count()
        return revs

