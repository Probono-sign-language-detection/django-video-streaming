from django.db import models

# Create your models here.
class Session(models.Model):
    session_id = models.IntegerField(primary_key=True)

class SessionData(models.Model):
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True)
    word = models.CharField(max_length=100)

    class Meta:
        unique_together = (("session", "id"),)