import csv
from django.core.management.base import BaseCommand
from core.models import Country
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Import countries from a CSV file into the Country model.'

    def handle(self, *args, **options):
        # Clear the Country table before import
        Country.objects.all().delete()
        self.stdout.write(self.style.WARNING('Country table cleared.'))

        csv_path = os.path.join(settings.BASE_DIR, 'core', 'external_data', 'countries.csv')
        with open(csv_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            count = 0
            for row in reader:
                try:
                    country_data = {
                        'id': int(row['id']) if row['id'] else None,
                        'name': row['name'].strip() if row['name'] else '',
                        'iso3': row.get('iso3') or None,
                        'iso2': row.get('iso2') or None,
                        'numeric_code': row.get('numeric_code') or None,
                        'phonecode': row.get('phonecode') or None,
                        'capital': row.get('capital') or None,
                        'currency': row.get('currency') or None,
                        'currency_name': row.get('currency_name') or None,
                        'currency_symbol': row.get('currency_symbol') or None,
                        'tld': row.get('tld') or None,
                        'native': row.get('native') or None,
                        'population': int(row['population']) if row.get('population') and row['population'].isdigit() else None,
                        'gdp': int(row['gdp']) if row.get('gdp') and row['gdp'].isdigit() else None,
                        'region': row.get('region') or None,
                        'region_id': int(row['region_id']) if row.get('region_id') and row['region_id'].isdigit() else None,
                        'subregion': row.get('subregion') or None,
                        'subregion_id': int(row['subregion_id']) if row.get('subregion_id') and row['subregion_id'].isdigit() else None,
                        'nationality': row.get('nationality') or None,
                        'area_sq_km': int(row['area_sq_km']) if row.get('area_sq_km') and row['area_sq_km'].isdigit() else None,
                        'postal_code_format': row.get('postal_code_format') or None,
                        'postal_code_regex': row.get('postal_code_regex') or None,
                        'timezones': row.get('timezones') or None,
                        'latitude': float(row['latitude']) if row.get('latitude') else None,
                        'longitude': float(row['longitude']) if row.get('longitude') else None,
                        'emoji': row.get('emoji') or None,
                        'emojiU': row.get('emojiU') or None,
                        'wikiDataId': row.get('wikiDataId') or None,
                    }
                    if country_data['name']:
                        Country.objects.create(**country_data)
                        count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Skipped row due to error: {e} | Row: {row}"))
            self.stdout.write(self.style.SUCCESS(f'Imported {count} countries.'))
