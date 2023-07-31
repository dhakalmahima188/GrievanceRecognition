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

class TextComplaint(models.Model):
    user=models.CharField(max_length=100)  
    complaint=models.CharField(max_length=100)
    complaint_time=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user
    


class AudioRecording(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio/',null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.title
