from django.urls import path
from . import views

urlpatterns = [
    path('paketlar/', views.PaketListView.as_view()),
    path('mening/', views.TolovListView.as_view()),
    path('yaratish/', views.tolov_yaratish),
    path('click/callback/', views.click_callback),
]