from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import MedicalRecord, Patient
from .serializers import MedicalRecordSerializer, PatientSerializer
from .permissions import IsDoctorOrAdmin

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrAdmin]

class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrAdmin]

    def get_queryset(self):
        return MedicalRecord.objects.filter(patient_id=self.kwargs['patient_pk'])
    
    def perform_create(self, serializer):
        try:
            patient = Patient.objects.get(id=self.kwargs['patient_pk'])
            serializer.save(patient=patient, created_by=self.request.user)
        except Patient.DoesNotExist:
            raise ValueError("Patient does not exist.")
        
class MyMedicalHistoryView(generics.ListAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MedicalRecord.objects.filter(patient__user=self.request.user).order_by('-visit_date')