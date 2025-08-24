from django.urls import path
from .views import DoctorListView, UserProfileView

urlpatterns = [
    path('doctors/', DoctorListView.as_view(), name='doctor-list'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
]