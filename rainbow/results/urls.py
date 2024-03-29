from django.urls import path, include

from rest_framework import routers
from results.views import region, prize

app_name = 'results'

router = routers.DefaultRouter()

router.register(r'results/region', region.RegionViewSet, basename="regions")
router.register(r'results/prize', prize.PrizeViewSet)
router.register(r'results/available_prize', prize.AvailablePrizeViewSet, basename='available_prize')
router.register(r'results/claimed_prize', prize.ClaimedPrizeViewSet, basename='claimed_prize')
