from django.urls import path, include

from rest_framework import routers
from results.views import region, prize

app_name = 'results'

router = routers.DefaultRouter()

router.register(r'region', region.RegionViewSet)
router.register(r'prize', prize.PrizeViewSet)
router.register(r'claimed_prize', prize.ClaimedPrizeViewSet)
