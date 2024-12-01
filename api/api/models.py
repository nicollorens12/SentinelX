from django.db import models

class FCMDevice(models.Model):
    registration_id = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    type = models.CharField(max_length=10, choices=[('ios', 'iOS'), ('android', 'Android')])

    def __str__(self):
        return f"{self.type} device - {self.registration_id}"
