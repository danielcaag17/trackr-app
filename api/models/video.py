from django.db import models
from .user import User


class Video(models.Model):
    id = models.CharField(
        primary_key=True,        # ⚠️ Le dices que este es el ID principal
        max_length=32,           # Limita la longitud
        unique=True,             # Garantiza que no se repita
        editable=False           # Opcional: evita que lo modifiquen en admin
    )
    title = models.CharField(max_length=255)
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    s3_url = models.URLField(max_length=500)
    public_url = models.URLField(max_length=500, default='https://s3-us-west-2.amazonaws.com')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('title', 'autor')
