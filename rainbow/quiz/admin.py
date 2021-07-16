from django.contrib import admin

from quiz.models import Quiz, QuizUser, Question, Answer, UserAnswer


class QuizAdmin(admin.ModelAdmin):
    list_display = ('name', )

class QuizUserAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user')

    def has_change_permission(self, request, obj=None):
        return False

class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'quiz')

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'correct')

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'correct', 'quiz_user')

    def has_change_permission(self, request, obj=None):
        return False


admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizUser, QuizUserAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer, AnswerAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
