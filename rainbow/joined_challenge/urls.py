# joined challenges
from rest_framework import routers

from joined_challenge.views import joined_challenge

router = routers.DefaultRouter()

app_name = 'joined_challenge'

router.register(r'joined_challenge/article_joined_challenge', joined_challenge.ArticleJoinedChallengeViewSet)
router.register(r'joined_challenge/event_participant_joined_challenge', joined_challenge.EventParticipantJoinedChallengeViewSet)
router.register(r'joined_challenge/school_gsa_joined_challenge', joined_challenge.SchoolGSAJoinedChallengeViewSet)
router.register(r'joined_challenge/event_organizer_joined_challenge', joined_challenge.EventOrganizerJoinedChallengeViewSet)
router.register(r'joined_challenge/story_joined_challenge', joined_challenge.StoryJoinedChallengeViewSet)
router.register(r'joined_challenge/project_joined_challenge', joined_challenge.ProjectJoinedChallengeViewSet)
router.register(r'joined_challenge/reacting_joined_challenge', joined_challenge.ReactingJoinedChallengeViewSet)
router.register(r'joined_challenge/support_joined_challenge', joined_challenge.SupportJoinedChallengeViewSet)
router.register(r'joined_challenge/quiz_joined_challenge', joined_challenge.QuizJoinedChallengeViewSet)
router.register(r'joined_challenge/custom_joined_challenge', joined_challenge.CustomJoinedChallengeViewSet)

