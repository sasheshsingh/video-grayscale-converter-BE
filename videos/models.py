from django.db import models

# Create your models here.
from django.db import models

class Video(models.Model):
    original_video = models.FileField(upload_to="uploads/")
    processed_video = models.FileField(upload_to="processed/", blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.original_video.name
