from django.db import models


class Tracker(models.Model):
    iou_threshold = models.FloatField()
    max_age = models.PositiveIntegerField()
    min_hits = models.PositiveIntegerField()
