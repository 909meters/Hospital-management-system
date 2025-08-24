from rest_framework import generics, permissions
from .models import CustomUser
from .serializers import DoctorSerializer, UserProfileSerializer
from patients.permissions import IsDoctorOrAdmin

class DoctorListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role=CustomUser.Role.DOCTOR)
    serializer_class = DoctorSerializer
    permission_classes = [permissions.IsAuthenticated]  # Allow all authenticated users to see doctors

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user