from django.urls import path
from . import views

urlpatterns = [
    path('', views.MashinaListView.as_view()),
    path('<int:pk>/', views.MashinaDetailView.as_view()),
    path('yaratish/', views.MashinaYaratishView.as_view()),
    path('mening/', views.MeningMashinalarimView.as_view()),
    path('<int:pk>/yangilash/', views.MashinaUpdateView.as_view()),
    path('<int:pk>/ochirish/', views.MashinaDeleteView.as_view()),
    path('<int:pk>/sotilgan/', views.sotilgan),
    path('<int:pk>/sevimli/', views.sevimli),
    path('sevimlilar/', views.SevimlilarView.as_view()),
]