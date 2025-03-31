from django.db import models

# each city the user adds
class City(models.Model):
    name = models.CharField(max_length=100, unique=True)     # can't add the same city twice
    added_at = models.DateTimeField(auto_now_add=True)       # when it got added
    def __str__(self):
        return self.name

# weather info tied to each city
class WeatherSnapshot(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='snapshots')  # link to one city
    temp = models.FloatField()                     # degrees celsius
    vibe = models.CharField(max_length=100)        # 'Clear', 'Rain', etc
    icon = models.CharField(max_length=200, blank=True, null=True)  # file name (from API)
    desc = models.TextField(blank=True)            # optional full description
    updated_at = models.DateTimeField(auto_now=True)  # last time it was fetched/updated

    def __str__(self):
        return f"{self.city.name}: {self.temp}°C – {self.vibe}"
