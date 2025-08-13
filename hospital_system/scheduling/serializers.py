from rest_framework import serializers
from .models import Appointment, DoctorSchedule
from patients.models import Patient

class AppointmentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.get_full_name', read_only=True)
    doctor_name = serializers.CharField(source='doctor.get_full_name', read_only=True)

    class Meta:
        model = Appointment
        fields = ('id', 'patient', 'patient_name', 'doctor', 'doctor_name', 'start_time', 'end_time', 'status', 'notes')
        read_only_fields = ['patient']

class DoctorScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSchedule
        fields = ('id', 'doctor', 'start_time', 'end_time')