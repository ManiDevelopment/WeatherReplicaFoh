from django.contrib import admin, messages
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response

from MySourceReplica.api_views import CityViewSet, SnapshotViewSet
from MySourceReplica.views import (
    WeatherPage,
    AddCityAjax,
    RemoveCityAjax,
    send_csrf_cookie,
    get_weather_data,
)

# Test route for popup messages
def msg_test(request):
    messages.success(request, "Flash works fine")
    return redirect('weather-home')

# Router for API endpoints
router = DefaultRouter()
router.register(r'cities', CityViewSet, basename='city')
router.register(r'snapshots', SnapshotViewSet, basename='snapshot')

# Root API listing
class APIRoot(APIView):
    def get(self, request):
        root = request.build_absolute_uri('/api/')
        return Response({
            'cities': f"{root}cities/",
            'snapshots': f"{root}snapshots/",
        })

urlpatterns = [
    path('admin/', admin.site.urls),

    # API
    path('api/', include(router.urls)),
    path('api/', APIRoot.as_view(), name='api-root'),

    # Web view
    path('', WeatherPage.as_view(), name='weather-home'),

    # AJAX endpoints
    path('ajax/add/', AddCityAjax.as_view(), name='add-city'),
    path('ajax/delete/<int:pk>/', RemoveCityAjax.as_view(), name='remove-city'),

    # Utility
    path('msg/', msg_test, name='test-msg'),
    path('csrf/', send_csrf_cookie, name='csrf-cookie'),
    path('proxy/<str:city_name>/', get_weather_data, name='weather-proxy'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
