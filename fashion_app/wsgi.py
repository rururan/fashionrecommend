import os
from django.core.wsgi import get_wsgi_application


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_app.settings')

application = get_wsgi_application()


from whitenoise.django import DjangoWhiteNoise #必要？
application = DjangoWhiteNoise(application)

