from django.shortcuts import render
from rest_framework import viewsets, permissions, generics
from .models import MedicalRecord, Patient
from .serializers import MedicalRecordSerializer, PatientSerializer
from .permissions import IsDoctorOrAdmin, CanViewPatients, CanViewMedicalRecords

class PatientViewSet(viewsets.ModelViewSet):
    serializer_class = PatientSerializer
    permission_classes = [permissions.IsAuthenticated, CanViewPatients]
    
    def get_queryset(self):
        user = self.request.user
        if user.role in ['DOCTOR', 'ADMIN']:
            # Doctors and admins can see all patients
            return Patient.objects.all()
        elif user.role == 'PATIENT':
            # Patients can only see their own profile
            return Patient.objects.filter(user=user)
        return Patient.objects.none()

class MedicalRecordViewSet(viewsets.ModelViewSet):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated, CanViewMedicalRecords]

    def get_queryset(self):
        patient_pk = self.kwargs['patient_pk']
        
        # If patient is requesting their own records, return them
        if self.request.user.role == 'PATIENT':
            if str(self.request.user.id) == str(patient_pk):
                return MedicalRecord.objects.filter(patient__user=self.request.user)
            else:
                return MedicalRecord.objects.none()
        
        # Doctors and admins can see all records for the patient
        return MedicalRecord.objects.filter(patient_id=patient_pk)
    
    def perform_create(self, serializer):
        # Only doctors and admins can create medical records
        if self.request.user.role not in ['DOCTOR', 'ADMIN']:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("Only doctors and admins can create medical records.")
            
        try:
            patient = Patient.objects.get(user_id=self.kwargs['patient_pk'])
            serializer.save(patient=patient, created_by=self.request.user)
        except Patient.DoesNotExist:
            raise ValueError("Patient does not exist.")
        
class MyMedicalHistoryView(generics.ListAPIView):
    serializer_class = MedicalRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return MedicalRecord.objects.filter(patient__user=self.request.user).order_by('-visit_date')