from django.urls import path, include

from rest_framework import routers
from results.views import region, prize

app_name = 'results'

router = routers.DefaultRouter()

router.register(r'results/region', region.RegionViewSet)
router.register(r'results/prize', prize.PrizeViewSet)
router.register(r'results/available_prize', prize.PrizeViewSet)
router.register(r'results/claimed_prize', prize.ClaimedPrizeViewSet)
