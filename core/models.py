from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from cryptography.fernet import Fernet, InvalidToken
import base64
from django.conf import settings
class UserAPIKey(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='openai_api_key')
    api_key_encrypted = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @staticmethod
    def get_fernet():
        key = getattr(settings, 'OPENAI_APIKEY_ENCRYPTION_KEY', None)
        if not key:
            raise Exception('OPENAI_APIKEY_ENCRYPTION_KEY must be set in settings.py')
        return Fernet(key)

    @property
    def api_key(self):
        if not self.api_key_encrypted:
            return ''
        try:
            f = self.get_fernet()
            return f.decrypt(base64.urlsafe_b64decode(self.api_key_encrypted)).decode()
        except (InvalidToken, Exception):
            return ''

    @api_key.setter
    def api_key(self, value):
        f = self.get_fernet()
        encrypted = f.encrypt(value.encode())
        self.api_key_encrypted = base64.urlsafe_b64encode(encrypted).decode()

    def __str__(self):
        return f"API Key for {self.user.email}"

from django.db import models
from django.contrib.auth.models import User

class Country(models.Model):

    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    iso3 = models.CharField(max_length=3, blank=True, null=True)
    iso2 = models.CharField(max_length=2, blank=True, null=True)
    numeric_code = models.CharField(max_length=10, blank=True, null=True)
    phonecode = models.CharField(max_length=10, blank=True, null=True)
    capital = models.CharField(max_length=100, blank=True, null=True)
    currency = models.CharField(max_length=10, blank=True, null=True)
    currency_name = models.CharField(max_length=50, blank=True, null=True)
    currency_symbol = models.CharField(max_length=10, blank=True, null=True)
    tld = models.CharField(max_length=10, blank=True, null=True)
    native = models.CharField(max_length=100, blank=True, null=True)
    population = models.BigIntegerField(blank=True, null=True)
    gdp = models.BigIntegerField(blank=True, null=True)
    region = models.CharField(max_length=50, blank=True, null=True)
    region_id = models.IntegerField(blank=True, null=True)
    subregion = models.CharField(max_length=50, blank=True, null=True)
    subregion_id = models.IntegerField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    area_sq_km = models.BigIntegerField(blank=True, null=True)
    postal_code_format = models.CharField(max_length=50, blank=True, null=True)
    postal_code_regex = models.CharField(max_length=200, blank=True, null=True)
    timezones = models.TextField(blank=True, null=True)
    latitude = models.DecimalField(max_digits=15, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=15, decimal_places=8, blank=True, null=True)
    emoji = models.CharField(max_length=10, blank=True, null=True)
    emojiU = models.CharField(max_length=20, blank=True, null=True)
    wikiDataId = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    career_stage = models.CharField(max_length=100)
    institution_name = models.CharField(max_length=200, default='Unknown')
    discipline = models.CharField(max_length=100, blank=True)
    ai_consent = models.BooleanField(default=False)

    def __str__(self):
        return f"Profile for {self.user.email} ({self.institution_name})"
