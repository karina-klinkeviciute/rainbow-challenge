# joined challenges
from rest_framework import routers

from joined_challenge.views import joined_challenge

router = routers.DefaultRouter()

app_name = 'joined_challenge'

router.register(r'article_joined_challenge', joined_challenge.ArticleJoinedChallengeViewSet)
router.register(r'event_participant_joined_challenge', joined_challenge.EventParticipantJoinedChallengeViewSet)
router.register(r'school_gsa_joined_challenge', joined_challenge.SchoolGSAJoinedChallengeViewSet)
router.register(r'event_organizer_joined_challenge', joined_challenge.EventOrganizerJoinedChallengeViewSet)
router.register(r'story_joined_challenge', joined_challenge.StoryJoinedChallengeViewSet)
router.register(r'project_joined_challenge', joined_challenge.ProjectJoinedChallengeViewSet)
router.register(r'reacting_joined_challenge', joined_challenge.ReactingJoinedChallengeViewSet)
router.register(r'support_joined_challenge', joined_challenge.SupportJoinedChallengeViewSet)
router.register(r'quiz_joined_challenge', joined_challenge.QuizJoinedChallengeViewSet)
router.register(r'custom_joined_challenge', joined_challenge.CustomJoinedChallengeViewSet)


urlpatterns = [
    # path('', include(router.urls)),

]
