from django.db import models
from django.conf import settings
from patients.models import Patient

class Appointment(models.Model):
    class AppointmentStatus(models.TextChoices):
        SCHEDULED = 'SCHEDULED', 'Scheduled'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointments',
        limit_choices_to={'role': 'DOCTOR'}
    )

    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=AppointmentStatus.choices,
        default=AppointmentStatus.SCHEDULED
    )
    notes = models.TextField(blank=True, null=True, help_text="Additional notes for the appointment")


class DoctorSchedule(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='schedule',
        limit_choices_to={'role': 'DOCTOR'}
    )
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"Schedule for Dr. {self.doctor.first_name} {self.doctor.last_name}: {self.start_time.strftime('%Y-%m-%d %H:%M')} - {self.end_time.strftime('%Y-%m-%d %H:%M')}"