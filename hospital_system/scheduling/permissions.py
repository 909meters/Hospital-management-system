from rest_framework import permissions

class IsOwnerOrDoctorOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_staff or request.user == obj.patient.user or request.user == obj.doctor
        return request.user.is_staff or request.user == obj.patient.user 