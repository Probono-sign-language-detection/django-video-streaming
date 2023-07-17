from django.db import models
from django.utils import timezone


# Create your models here.
class Session(models.Model):
    session_id = models.IntegerField(primary_key=True, default=1)
    created_at = models.DateTimeField(auto_now_add=True, default=timezone.now)

class SessionData(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=100, blank=True)

    class Meta:
        unique_together = (("session", "id"),)