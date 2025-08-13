from rest_framework_nested import routers
from .views import MedicalRecordViewSet, MyMedicalHistoryView
from django.urls import path, include

router = routers.SimpleRouter()

records_router = routers.NestedSimpleRouter(router, r'patients', lookup='patient')
records_router.register(r'records', MedicalRecordViewSet, basename='patient-records')

urlpatterns += [ 
    path('my-medical-history/', MyMedicalHistoryView.as_view(), name='my-medical-history'),
]