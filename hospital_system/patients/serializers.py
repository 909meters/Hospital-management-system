from rest_framework import serializers
from .models import MedicalRecord

class MedicalRecordSerializer(serializers.ModelSerializer):
    create_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = MedicalRecord
        fields = ('id', 'visit_date', 'diagnosis', 'treatment', 'notes', 'patient', 'created_by', 'create_by_name')
        read_only_fields = ['created_by']