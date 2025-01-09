import os
import sys
from django.core.wsgi import get_wsgi_application

# Django ayarlarını tanımla
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Sanal ortamın bulunduğu dizini sys.path'e ekleyin
sys.path.append('/home/ubuntu/algi-web-studio')

# .env dosyasını yüklemeyi dene
try:
    from dotenv import load_dotenv
    load_dotenv()  # .env dosyasını yükle
except ImportError:
    pass  # Eğer dotenv modülü yoksa hata vermesin, pas geç

# WSGI uygulamasını başlat
application = get_wsgi_application()
