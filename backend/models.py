from django.db import models
from .predictor import make_prediction  # Adjust the import path


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
    #complain_id=models.AutoField(primary_key=True,default=5)
    user=models.CharField(max_length=100)  
    complaint=models.CharField(max_length=100)
    complaint_time=models.DateTimeField(auto_now_add=True)
    location=models.CharField(max_length=100,default='Butwal')
    province=models.CharField(max_length=100,default=7)
    district=models.CharField(max_length=100,default='Rupandehi')
    municipality=models.CharField(max_length=100,default='Suddhodhan')
    wardno=models.CharField(max_length=100,default=4)
    status=models.CharField(max_length=100,default='pending')
    criticality=models.CharField(max_length=100,default='low')
    complain_tag=models.IntegerField(default=0)
    predicted_class = models.CharField(max_length=100, blank=True, null=True)
        
    def __str__(self):
        return self.user
    


class AudioRecording(models.Model):
    title = models.CharField(max_length=100)
    audio_file = models.FileField(upload_to='audio/',null=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self):
        return self.title
    

class StatusTable(models.Model):
    complain_id=models.ForeignKey(TextComplaint,on_delete=models.CASCADE)
    user=models.CharField(max_length=100)
    status=models.CharField(max_length=100)
    problem=models.CharField(max_length=100)
    miistry=models.CharField(max_length=100)
   
    def __str__(self):
        return self.user

class Category(models.Model):
    category=models.CharField(max_length=100)
    category_tag=models.IntegerField()
    def __str__(self):
        return self.category