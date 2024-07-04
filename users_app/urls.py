from django.urls import path
from .views import RegisterAPIView, VerifyAPIView, LoginAPIView, MyTokenObtainPairView, NotesAPIView, ProfileAPIView
from rest_framework_simplejwt import views as jwt_views


urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='create'),
    path('verify/', VerifyAPIView.as_view(), name='verify'),
    path('login/', LoginAPIView.as_view(), name='login'),
    
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', ProfileAPIView.as_view(), name='profile'),
    path('notes/', NotesAPIView.as_view(), name='notes'),
    path('notes/<str:id>/', NotesAPIView.as_view(), name='notes'),
]


