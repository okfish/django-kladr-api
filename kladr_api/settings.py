from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

KLADR_API_URL = getattr(settings, 'KLADR_API_URL', 'https://kladr-api.ru/api.php')
KLADR_API_TOKEN = getattr(settings, 'KLADR_API_TOKEN', None)
    
if not KLADR_API_TOKEN:
    raise ImproperlyConfigured("""API token are required. 
                                Please, check project settings for the KLADR_API_TOKEN. 
                                """)
