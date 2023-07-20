from django.db import models

# Create your models here.
class CallRecord(models.Model):
    user=models.CharField(max_length=100)
    phone_number=models.CharField(max_length=100)
    call_type=models.CharField(max_length=100)
    call_duration=models.CharField(max_length=100)
    call_date=models.CharField(max_length=100)
    call_time=models.CharField(max_length=100)

    def __str__(self):
        return self.user
