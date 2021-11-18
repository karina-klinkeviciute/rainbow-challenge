from django.urls import path

from joined_challenge.views.joined_challenge import UserJoinedChallengesAPIView
from results.views.prize import UserClaimedPrizesAPIView
from user import views
from user.views import UserActivationView

urlpatterns = [
    path('gender/', views.GenderListView.as_view(), name='gender-list'),
    path('received_prizes', UserClaimedPrizesAPIView.as_view(), name='user-prize-list'),
    path('joined_challenges', UserJoinedChallengesAPIView.as_view(), name='user-joined-challenges'),
    path('completed_challenges', UserJoinedChallengesAPIView.as_view(), name='user-completed-challenges'),
    path('activate/<uid>/<token>', UserActivationView.as_view(), name='user-completed-challenges')

]
