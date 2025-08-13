from django.shortcuts import render
from rest_framework import generics
from .models import CustomUser
from .serializers import DoctorSerializer

class DoctorListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role=CustomUser.Role.DOCTOR)
    serializer_class = DoctorSerializer