from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)
class Slot(models.Model):
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='slots')
    start_time = models.DateTimeField()
    is_booked = models.BooleanField(default=False)
class Booking(models.Model):
    patient = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.OneToOneField(Slot, on_delete=models.CASCADE)