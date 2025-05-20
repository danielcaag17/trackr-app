from django.db import models
from .user import User


class Video(models.Model):
    id = models.CharField(primary_key=True, max_length=32, unique=True, editable=False)
    title = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    s3_url = models.URLField(max_length=500)
    public_url = models.URLField(max_length=500, default='https://s3-us-west-2.amazonaws.com')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    '''
    for now this, later when managing users, there would not be the default.
    Now two random people cannot upload a video named equally
    class Meta:
        {title, autor}
    '''
