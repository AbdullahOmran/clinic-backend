from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView 
from .views import MyTokenObtainPairView
from .views import Register

from rest_framework_swagger.views import get_swagger_view
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Medcy API",
        default_version='v1',),
    public=True,
    permission_classes=(permissions.AllowAny,),
)
urlpatterns = [
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0),name='schema-swagger-ui'),
    # path('', views.getRoutes),
    path('auth/login/', MyTokenObtainPairView.as_view(), name = 'token_obtain_pair'),
    path('auth/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    path('auth/register/', Register.as_view(), name = 'auth-register'),
    path('user/',views.user_details),
    path('doctor/',views.doctor_details),
    path('secretary/',views.secretary_details),
    path('patient/<int:pk>/',views.patient_details),
    path('patient/',views.create_or_patient_list),
    path('appointment/<int:pk>/',views.appointment_details),
    path('appointment/',views.create_or_appointment_list),
    path('treatment/<int:pk>/',views.treatment_details),
    path('treatment/',views.create_or_treatment_list),
    path('clinic/<int:pk>/',views.clinic_details),
    
]