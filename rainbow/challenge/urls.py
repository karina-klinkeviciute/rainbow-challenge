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

from challenge.views import challenge_api
from challenge.views.challenge import ArticleChallengeView, ArticleChallengeListView
from results.views.region import RegionChallengesAPIView, RegionUsersAPIView

router = routers.DefaultRouter()

app_name = 'challenge'

router.register(r'challenge/challenge', challenge_api.ChallengeViewSet)
router.register(r'challenge/article_challenge', challenge_api.ArticleChallengeViewSet)
router.register(r'challenge/event_participant_challenge', challenge_api.EventParticipantChallengeViewSet)
router.register(r'challenge/school_gsa_challenge', challenge_api.SchoolGSAChallengeViewSet)
router.register(r'challenge/event_organizer_challenge', challenge_api.EventOrganizerChallengeViewSet)
router.register(r'challenge/story_challenge', challenge_api.StoryChallengeViewSet)
router.register(r'challenge/project_challenge', challenge_api.ProjectChallengeViewSet)
router.register(r'challenge/reacting_challenge', challenge_api.ReactingChallengeViewSet)
router.register(r'challenge/support_challenge', challenge_api.SupportChallengeViewSet)
router.register(r'challenge/quiz_challenge', challenge_api.QuizChallengeViewSet)
router.register(r'challenge/custom_challenge', challenge_api.CustomChallengeViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('challenge/article-challenge/<uuid>/', ArticleChallengeView.as_view(), name='article-update'),
    path('challenge/article-challenge/', ArticleChallengeView.as_view(), name='article-create'),
    path('challenge/article-challenges/', ArticleChallengeListView.as_view(), name='articles')
]
