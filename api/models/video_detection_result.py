from django.db import models
from .user import User
from .video import Video


class VideoDetectionResult(models.Model):
    title = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    s3_url = models.URLField(max_length=500)
    original_video = models.ForeignKey(Video, on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    stat1 = models.CharField(max_length=3)
    # Todo add stats

    class Meta:
        unique_together = ('title', 'autor')
