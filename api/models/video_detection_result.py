from django.db import models
from .ml_model import MLModel
from .user import User
from .video import Video
from .tracker import Tracker


class VideoDetectionResult(models.Model):
    title = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    s3_url = models.URLField(max_length=500)
    original_video = models.ForeignKey(Video, on_delete=models.CASCADE)
    public_url = models.URLField(max_length=500, default='https://s3-us-west-2.amazonaws.com')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    tracker = models.ForeignKey(Tracker, on_delete=models.CASCADE, default=1)
    ml_model = models.ForeignKey(MLModel, on_delete=models.CASCADE, default=1)

    # Basic stats
    frame_processed = models.IntegerField(default=0, null=True, blank=True)
    confidence_threshold = models.FloatField(default=0, null=True)
    video_duration = models.FloatField(default=0, null=True)
    processing_time_seconds = models.FloatField(default=0, null=True)
    video_fps = models.IntegerField(default=0, null=True)

    # Global Metrics
    total_detections = models.IntegerField(default=0, null=True)
    detections_discarded = models.IntegerField(default=0, null=True)
    frames_with_detections = models.IntegerField(default=0, null=True)
    avg_confidence = models.FloatField(default=0, null=True)
    avg_people_per_frame = models.FloatField(default=0, null=True)
    person_presence_percent = models.FloatField(default=0, null=True)
    people_detected = models.IntegerField(default=0, null=True)

    # Detection Peaks
    peak_frame_id = models.IntegerField(default=0, null=True)
    peak_count = models.IntegerField(default=0, null=True)

    # More complex data
    detections_per_frame = models.JSONField(default=list)
    time_per_person = models.JSONField(default=dict)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'autor', 'ml_model')
