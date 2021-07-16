from rest_framework import routers
from django.urls import path, include

from quiz.views import QuizViewSet, QuizUserViewSet, QuestionViewSet, AnswerViewSet, UserAnswerViewSet

router = routers.DefaultRouter()

app_name = 'quiz'

router.register(r'quiz', QuizViewSet)
router.register(r'quiz-user', QuizUserViewSet)
router.register(r'question', QuestionViewSet)
router.register(r'answer', AnswerViewSet)
router.register(r'user-answer', UserAnswerViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
