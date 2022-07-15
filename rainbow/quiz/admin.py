from django.contrib import admin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin

from quiz.models import Quiz, QuizUser, Question, Answer, UserAnswer


class AnswerInline(NestedStackedInline):
    model = Answer
    extra = 1
    fk_name = 'question'

class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    fk_name = 'quiz'
    inlines = (AnswerInline, )

class QuizAdmin(NestedModelAdmin):
    list_display = ('name', )
    inlines = (QuestionInline, )

class QuizUserAdmin(admin.ModelAdmin):
    list_display = ('quiz', 'user')
    readonly_fields = ('correct_answers_count', )

    def has_change_permission(self, request, obj=None):
        return False

class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question', 'correct')



class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question', 'quiz')
    inlines = (AnswerInline, )

class UserAnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'quiz_user')
    readonly_fields = ('is_correct', )

    def has_change_permission(self, request, obj=None):
        return False


# admin.site.register(Quiz, QuizAdmin)
# admin.site.register(QuizUser, QuizUserAdmin)
# admin.site.register(Question, QuestionAdmin)
# admin.site.register(Answer, AnswerAdmin)
# admin.site.register(UserAnswer, UserAnswerAdmin)
