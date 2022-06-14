from django.db import models

# Create your models here.

class video(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    upload = models.FileField()