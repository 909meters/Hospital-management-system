from rest_framework import permissions

class IsDoctorOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return request.user.role in ['DOCTOR', 'ADMIN']

class CanViewPatients(permissions.BasePermission):
    """
    Patients can view only their own profile.
    Doctors and admins can view all patients and create new patients.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # For write operations (POST, PUT, PATCH, DELETE), only doctors and admins are allowed
        if request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            return request.user.role in ['DOCTOR', 'ADMIN']
        
        # For read operations (GET), all authenticated users can access
        return True
        
    def has_object_permission(self, request, view, obj):
        # For write operations, only doctors and admins
        if request.method in ['PUT', 'PATCH', 'DELETE']:
            return request.user.role in ['DOCTOR', 'ADMIN']
            
        # For read operations
        if request.user.role in ['DOCTOR', 'ADMIN']:
            return True
        # Patients can only see their own data
        return request.user.role == 'PATIENT' and obj.user == request.user

class CanViewMedicalRecords(permissions.BasePermission):
    """
    Patients can view only their own medical records.
    Doctors and admins can view all medical records.
    """
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        
        # For nested routes like /patients/{id}/records/, check if patient matches current user
        if request.user.role == 'PATIENT':
            patient_pk = view.kwargs.get('patient_pk')
            if patient_pk:
                # Patient can only access their own records
                return str(request.user.id) == str(patient_pk)
        
        # Doctors and admins can access all records
        return request.user.role in ['DOCTOR', 'ADMIN', 'PATIENT']
        
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['DOCTOR', 'ADMIN']:
            return True
        # Patients can only see their own medical records
        return request.user.role == 'PATIENT' and obj.patient.user == request.user