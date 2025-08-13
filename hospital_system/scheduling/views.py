from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Appointment, DoctorSchedule
from .serializers import AppointmentSerializer, DoctorScheduleSerializer
from patients.models import Patient
from .permissions import IsOwnerOrDoctorOrAdmin

class AppointmentListCreateView(generics.ListCreateAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'PATIENT':
            return Appointment.objects.filter(patient__user=user)
        elif user.role == 'DOCTOR':
            return Appointment.objects.filter(doctor=user)
        elif user.role == 'ADMIN':
            # Admin can see all appointments
            return Appointment.objects.all()

        return Appointment.objects.none()
    
    def perform_create(self, serializer):
        try:
            patient_profile = Patient.objects.get(user=self.request.user)
            if self.request.user.role != 'PATIENT':
                raise ValueError("Only patients can create appointments.")
            serializer.save(patient=patient_profile)
        except Patient.DoesNotExist:
            raise ValueError("Patient profile does not exist for the current user.")
        

class AppointmentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrDoctorOrAdmin]


class DoctorScheduleListView(generics.ListAPIView):
    queryset = DoctorSchedule.objects.all()
    serializer_class = DoctorScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]