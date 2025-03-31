from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.decorators.http import require_GET
import requests
from .models import City
from .forms import CityForm

DEFAULT_CITIES = ['Tokyo', 'London', 'Guildford']
API_KEY = 'GCJSPTBRLERKVDUSZFJZZTL7Y'

# Checks if a city is real by querying the weather API
def city_exists(name):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{name}?unitGroup=metric&key={API_KEY}&contentType=json"
    try:
        r = requests.get(url, timeout=6)
        r.raise_for_status()
        return True
    except requests.RequestException:
        return False

# CSRF cookie setter
@csrf_exempt
@require_GET
@ensure_csrf_cookie
def send_csrf_cookie(request):
    return JsonResponse({'message': 'csrf cookie set'})

# External API proxy
@csrf_exempt
@require_GET
def get_weather_data(request, city_name):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city_name}?unitGroup=metric&key={API_KEY}&contentType=json"
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        return JsonResponse(r.json())
    except requests.RequestException as err:
        return JsonResponse({'error': 'weather fetch failed', 'details': str(err)}, status=500)

# Main page
class WeatherPage(ListView):
    model = City
    template_name = 'weather.html'
    context_object_name = 'cities'

    def get_queryset(self):
        if not City.objects.exists():
            for name in DEFAULT_CITIES:
                City.objects.get_or_create(name=name)
        return City.objects.all().order_by('added_at')

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        for city in ctx['cities']:
            city.snap_count = city.snapshots.count()
        return ctx

# AJAX city adder with validation
class AddCityAjax(View):
    @csrf_exempt
    def post(self, request, *args, **kwargs):
        form = CityForm(request.POST)
        if form.is_valid():
            raw_name = form.cleaned_data['name']
            name = raw_name.strip().title()  # consistent casing

            # 1. Check for duplicates case-insensitively
            if City.objects.filter(name__iexact=name).exists():
                return JsonResponse({
                    'status': 'fail',
                    'errors': f"City `{raw_name}` already exists in the list!"
                }, status=400)

            # 2. Then check with normalised name if it's real
            if not city_exists(name):
                return JsonResponse({
                    'status': 'fail',
                    'errors': f"City `{raw_name}` does not exist in the world!"
                }, status=400)

            # 3. Save it with clean casing
            city = City.objects.create(name=name)
            return JsonResponse({'status': 'ok', 'city': {'id': city.id, 'name': city.name}})

        return JsonResponse({
            'status': 'fail',
            'errors': 'Please enter a valid city name.'
        }, status=400)

# AJAX city remover
class RemoveCityAjax(View):
    def post(self, request, pk, *args, **kwargs):
        return self.delete(request, pk)

    def delete(self, request, pk, *args, **kwargs):
        city = City.objects.filter(pk=pk).first()
        if not city:
            return JsonResponse({'status': 'fail', 'msg': 'City not found'}, status=404)
        city.delete()
        return JsonResponse({'status': 'ok'})
