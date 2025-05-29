from django.db import models
from .user import User


class Video(models.Model):
    id = models.CharField(primary_key=True, max_length=32, unique=True, editable=False)
    title = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    s3_url = models.URLField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    '''
    For now this (an autor can upload the same video several times)
    Later, when managing users, there would not be the default user.
    Now two random users cannot upload a video named equally for this reason (two random users uses the default user)
    class Meta:
        unique_together = ('title', 'autor')
    '''
