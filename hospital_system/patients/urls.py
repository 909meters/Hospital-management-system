from django.urls import path
from rest_framework_nested import routers
from .views import MedicalRecordViewSet, MyMedicalHistoryView, PatientViewSet

router = routers.SimpleRouter()
router.register(r'', PatientViewSet, basename='patients')

records_router = routers.NestedSimpleRouter(router, r'', lookup='patient')
records_router.register(r'(?P<patient_pk>[^/.]+)/records', MedicalRecordViewSet, basename='patient-records')



urlpatterns = [
    path('my-history/', MyMedicalHistoryView.as_view(), name='my-medical-history'),
] + router.urls + records_router.urls