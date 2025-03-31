# API viewsets for My Weather Replica

from .serializers import CitySerializer, SnapshotSerializer
from .models import City, WeatherSnapshot
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from rest_framework.decorators import action

# handle full weather snapshot CRUD
class SnapshotViewSet(viewsets.ModelViewSet):
    queryset = WeatherSnapshot.objects.all().order_by('-updated_at')
    serializer_class = SnapshotSerializer
    permission_classes = [permissions.AllowAny]

    # GET /api/snapshots/latest/<city_id>/
    @action(detail=False, methods=['get'], url_path='latest/(?P<city_id>[^/.]+)')
    def latest_for_city(self, request, city_id=None):
        city = get_object_or_404(City, pk=city_id)
        snap = city.snapshots.order_by('-updated_at').first()
        if not snap:
            raise ValidationError("No weather data for this city.")
        return Response(self.get_serializer(snap).data)

# handle city list / create / get-by-name
class CityViewSet(viewsets.ModelViewSet):
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return City.objects.all().order_by('name')

    # GET /api/cities/by-name/<name>/
    @action(detail=False, methods=['get'], url_path='by-name/(?P<name>[^/.]+)')
    def get_by_name(self, request, name=None):
        city = get_object_or_404(City, name__iexact=name)
        return Response(self.get_serializer(city).data)