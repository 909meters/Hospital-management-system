from rest_framework import serializers
from .models import MedicalRecord, Patient
from users.models import CustomUser
import uuid

class PatientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='user.get_full_name', read_only=True)
    user_id = serializers.ReadOnlyField()
    
    # Fields for creating a new patient
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)
    email = serializers.EmailField(write_only=True, required=False)
    
    class Meta:
        model = Patient
        fields = (
            'user_id', 'full_name', 'date_of_birth', 'address', 'phone_number',
            'first_name', 'last_name', 'email'
        )
    
    def create(self, validated_data):
        # Extracting first name, last name, and email from validated data
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')
        email = validated_data.pop('email', '')
        
        # Creating a unique username for the patient
        base_username = f"patient_{first_name.lower()}_{last_name.lower()}"
        username = base_username
        counter = 1
        
        # Ensuring the username is unique
        while CustomUser.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1

        # Creating the user
        user = CustomUser.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            role='PATIENT'
        )
        
        # Creating the patient instance
        patient = Patient.objects.create(user=user, **validated_data)
        return patient


class MedicalRecordSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)

    class Meta:
        model = MedicalRecord
        fields = ('id', 'visit_date', 'diagnosis', 'treatment', 'notes', 'patient', 'created_by', 'created_by_name')
        read_only_fields = ['created_by', 'patient']