from django.contrib import admin
from .models import TextComplaint,AudioRecording,StatusTable,Category
admin.site.site_header = 'Greviance Management System'
admin.site.register(TextComplaint)
admin.site.register(AudioRecording)
admin.site.register(StatusTable)
admin.site.register(Category)
# Register your models here.
