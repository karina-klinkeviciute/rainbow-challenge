from rest_framework import routers
from django.urls import path, include

from quiz.views import QuizViewSet, QuizUserViewSet, QuestionViewSet, AnswerViewSet, UserAnswerViewSet

router = routers.DefaultRouter()

app_name = 'quiz'

router.register(r'quiz/quiz', QuizViewSet)
router.register(r'quiz/quiz-user', QuizUserViewSet)
router.register(r'quiz/question', QuestionViewSet)
router.register(r'quiz/answer', AnswerViewSet)
router.register(r'quiz/user-answer', UserAnswerViewSet)
