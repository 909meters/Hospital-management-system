from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import DoctorSerializer
from patients.permissions import IsDoctorOrAdmin

class DoctorListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role=CustomUser.Role.DOCTOR)
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated, IsDoctorOrAdmin]