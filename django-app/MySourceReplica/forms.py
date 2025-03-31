from django import forms
from .models import WeatherSnapshot, City

# form for editing a weather snapshot (if needed)
class SnapshotForm(forms.ModelForm):
    class Meta:
        model = WeatherSnapshot
        fields = ['city', 'temp', 'vibe', 'icon', 'desc']

    def clean_temp(self):
        t = self.cleaned_data.get('temp')
        if t is not None and (t < -100 or t > 100):
            raise forms.ValidationError("Temp must be between -100 and 100°C.")
        return t

    def clean_vibe(self):
        vibe = self.cleaned_data.get('vibe', '').strip()
        if not vibe:
            raise forms.ValidationError("Enter a weather condition.")
        return vibe

# form for adding new cities
class CityForm(forms.ModelForm):
    class Meta:
        model = City
        fields = ['name']

    def clean_name(self):
        raw = self.cleaned_data.get('name', '')
        return raw.strip()