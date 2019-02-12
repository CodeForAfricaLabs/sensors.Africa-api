from rest_framework import routers

from .views import SensorDataStatView

router = routers.DefaultRouter()

router.register(r"(?P<sensor_type>[air]+)/data/(?P<city_slug>[\w-]+)", SensorDataStatView)

api_urls = router.urls
