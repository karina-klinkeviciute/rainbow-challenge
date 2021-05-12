"""rainbow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include

from rest_framework import routers
from challenge import views

router = routers.DefaultRouter()
# challenges
router.register(r'challenge', views.ChallengeViewSet)
router.register(r'article_challenge', views.ArticleChallengeViewSet)
router.register(r'event_participant_challenge', views.EventParticipantChallengeViewSet)
router.register(r'school_gsa_challenge', views.SchoolGSAChallengeViewSet)
router.register(r'event_organizer_challenge', views.EventOrganizerChallengeViewSet)
router.register(r'story_challenge', views.StoryChallengeViewSet)

# joined challenges
router.register(r'article_joined_challenge', views.ArticleJoinedChallengeViewSet)
router.register(r'event_participant_joined_challenge', views.EventParticipantJoinedChallengeViewSet)
router.register(r'school_gsa_joined_challenge', views.SchoolGSAJoinedChallengeViewSet)
router.register(r'event_organizer_joined_challenge', views.EventOrganizerJoinedChallengeViewSet)
router.register(r'story_joined_challenge', views.StoryJoinedChallengeViewSet)

router.register(r'region', views.RegionViewSet)
router.register(r'prize', views.PrizeViewSet)
router.register(r'claimed_prize', views.ClaimedPrizeViewSet)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('region/<region_uuid>/challenge/', views.RegionChallengesAPIView.as_view(), name='region-user-list'),
    path('region/<region_uuid>/user/', views.RegionUsersAPIView.as_view(), name='region-user-list'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
