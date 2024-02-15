from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import MyTokenObtainPairView


urlpatterns = [
    path('', views.getRoutes),
    path('token/', MyTokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('user/<int:pk>/',views.user_details),
    path('doctor/<int:pk>/',views.doctor_details),
    path('secretary/<int:pk>/',views.secretary_details),
    path('patient/<int:pk>/',views.patient_details),
    path('appointment/<int:pk>/',views.appointment_details),
    
]