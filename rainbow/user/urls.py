from django.urls import path

from joined_challenge.views.joined_challenge import UserJoinedChallengesAPIView, UserCompletedChallengesAPIView
from user import views
from user.views import OAuthStateCodeToken

urlpatterns = [
    path('gender/', views.GenderListView.as_view(), name='gender-list'),
    path('joined_challenges', UserJoinedChallengesAPIView.as_view(), name='user-joined-challenges'),
    path('completed_challenges', UserCompletedChallengesAPIView.as_view(), name='user-completed-challenges'),
    path('oauth_token/', OAuthStateCodeToken.as_view(), name='oauth-token-get'),
]
