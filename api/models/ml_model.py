from django.db import models


class ModelMetrics(models.Model):
    # Training loss
    train_box_loss = models.FloatField(null=True, blank=True)
    train_cls_loss = models.FloatField(null=True, blank=True)
    train_dfl_loss = models.FloatField(null=True, blank=True)

    # Validation loss
    val_box_loss = models.FloatField(null=True, blank=True)
    val_cls_loss = models.FloatField(null=True, blank=True)
    val_dfl_loss = models.FloatField(null=True, blank=True)
    val_precision = models.FloatField(null=True, blank=True)
    val_recall = models.FloatField(null=True, blank=True)
    val_map50 = models.FloatField(null=True, blank=True)
    val_map50_95 = models.FloatField(null=True, blank=True)


class MLModel(models.Model):
    model_name = models.CharField(max_length=32)
    description = models.TextField()
    metrics = models.OneToOneField(
        ModelMetrics, on_delete=models.SET_NULL, null=True, blank=True, related_name='ml_model'
    )

    def __str__(self):
        return self.model_name
