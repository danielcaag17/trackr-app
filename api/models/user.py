from django.db import models


class User(models.Model):
    user = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
