from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RoyxatView, ProfilView

urlpatterns = [
    path('royxat/', RoyxatView.as_view()),
    path('kirish/', TokenObtainPairView.as_view()),
    path('token/yangilash/', TokenRefreshView.as_view()),
    path('profil/', ProfilView.as_view()),
]