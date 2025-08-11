from django.db import models
from django.conf import settings

class Patient(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, primary_key=True)

    date_of_birth = models.DateField()
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=30)

    def __str__(self):
        return f"Patient: {self.user.first_name} {self.user.last_name}"
    
class MedicalRecord(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_records')

    visit_date = models.DateTimeField(auto_now_add=True)
    diagnosis = models.CharField(max_length=255)
    treatment = models.TextField()
    notes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Record for {self.patient.user.username} on {self.visit_date.strftime('%Y-%m-%d %H:%M:%S')}"