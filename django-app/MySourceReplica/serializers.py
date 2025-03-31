# serializers.py — deals with how we shape up data for API use

from rest_framework import serializers
from .models import WeatherSnapshot, City

# handles the actual weather snapshot data
class SnapshotSerializer(serializers.ModelSerializer):
    city_name = serializers.ReadOnlyField(source='city.name')

    class Meta:
        model = WeatherSnapshot
        fields = ['id', 'city', 'city_name', 'temp', 'vibe', 'icon', 'desc', 'updated_at']
        read_only_fields = ['city_name', 'updated_at']

# handles city info (name, added date, and linked weather)
class CitySerializer(serializers.ModelSerializer):
    weather_entries = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = City
        fields = ['id', 'name', 'added_at', 'weather_entries']
        read_only_fields = ['added_at', 'weather_entries']

    # grabs the latest weather snapshots for this city
    def get_weather_entries(self, obj):
        snaps = obj.snapshots.all().order_by('-updated_at')
        return SnapshotSerializer(snaps, many=True).data