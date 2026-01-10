from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Avto Elon API",
        default_version='v1',
        description="Avtomobil e'lonlari mobile ilova uchun API dokumentatsiyasi",
        contact=openapi.Contact(email="support@avtoelon.uz"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),

    # API endpoints
    path('api/auth/', include('apps.users.urls')),
    path('api/mashinalar/', include('apps.cars.urls')),
    path('api/tolovlar/', include('apps.payments.urls')),

    # API dokumentatsiya
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='redoc'),
    path('swagger.json', schema_view.without_ui(cache_timeout=0), name='swagger-json'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)