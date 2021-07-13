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

from challenge.views import challenge
from joined_challenge.views import joined_challenge
from results.views import region, prize
from results.views.region import RegionChallengesAPIView, RegionUsersAPIView

router = routers.DefaultRouter()
# challenges
router.register(r'challenge', challenge.ChallengeViewSet)
router.register(r'article_challenge', challenge.ArticleChallengeViewSet)
router.register(r'event_participant_challenge', challenge.EventParticipantChallengeViewSet)
router.register(r'school_gsa_challenge', challenge.SchoolGSAChallengeViewSet)
router.register(r'event_organizer_challenge', challenge.EventOrganizerChallengeViewSet)
router.register(r'story_challenge', challenge.StoryChallengeViewSet)
router.register(r'project_challenge', challenge.ProjectChallengeViewSet)
router.register(r'reacting_challenge', challenge.ReactingChallengeViewSet)
router.register(r'support_challenge', challenge.SupportChallengeViewSet)

# joined challenges
router.register(r'article_joined_challenge', joined_challenge.ArticleJoinedChallengeViewSet)
router.register(r'event_participant_joined_challenge', joined_challenge.EventParticipantJoinedChallengeViewSet)
router.register(r'school_gsa_joined_challenge', joined_challenge.SchoolGSAJoinedChallengeViewSet)
router.register(r'event_organizer_joined_challenge', joined_challenge.EventOrganizerJoinedChallengeViewSet)
router.register(r'story_joined_challenge', joined_challenge.StoryJoinedChallengeViewSet)
router.register(r'project_joined_challenge', joined_challenge.ProjectJoinedChallengeViewSet)
router.register(r'reacting_joined_challenge', joined_challenge.ReactingJoinedChallengeViewSet)
router.register(r'support_joined_challenge', joined_challenge.SupportJoinedChallengeViewSet)

router.register(r'region', region.RegionViewSet)
router.register(r'prize', prize.PrizeViewSet)
router.register(r'claimed_prize', prize.ClaimedPrizeViewSet)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('region/<region_uuid>/challenge/', RegionChallengesAPIView.as_view(), name='region-user-list'),
    path('region/<region_uuid>/user/', RegionUsersAPIView.as_view(), name='region-user-list'),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
