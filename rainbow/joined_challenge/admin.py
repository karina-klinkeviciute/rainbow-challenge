from django.contrib import admin
from import_export.admin import ExportMixin
from import_export.resources import ModelResource

from joined_challenge.models import JoinedChallenge, ArticleJoinedChallenge, EventParticipantJoinedChallenge, \
    SchoolGSAJoinedChallenge, EventOrganizerJoinedChallenge, StoryJoinedChallenge, ProjectJoinedChallenge, \
    ReactingJoinedChallenge, SupportJoinedChallenge, CustomJoinedChallenge, QuizJoinedChallenge
from joined_challenge.models.base import JoinedChallengeFile
from joined_challenge.models.quiz import UserAnswer


class JoinedChallengeResource(ModelResource):

    class Meta:
        model = JoinedChallenge
        fields = ("challenge__name", 'user__email', 'joined_at', 'completed_at', 'status', )


class JoinedChallengeAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('user', 'challenge', 'status', )
    list_filter = ('status', )
    fields = ('user', 'challenge', 'status', 'joined_at', 'completed_at', "files_admin")
    readonly_fields = ('joined_at', "files_admin")
    resource_class = JoinedChallengeResource

class JoinedChallengeFileAdmin(admin.ModelAdmin):
    list_display = ('joined_challenge', "file")


class ExportableJoinedChallengeAdmin(ExportMixin, admin.ModelAdmin):
    pass


class ArticleJoinedChallengeAdmin(ExportableJoinedChallengeAdmin):
    list_display = ('main_joined_challenge', 'article_name', 'article_url')


class EventParticipantJoinedChallengeAdmin(ExportableJoinedChallengeAdmin):
    list_display = ('main_joined_challenge', )


class SchoolGSAJoinedChallengeAdmin(ExportableJoinedChallengeAdmin):
    list_display = ('main_joined_challenge', )


class EventOrganizerJoinedChallengeAdmin(ExportableJoinedChallengeAdmin):
    list_display = ('main_joined_challenge', 'event_name')


class StoryJoinedChallengeAdmin(ExportableJoinedChallengeAdmin):
    list_display = ('main_joined_challenge', )


class ProjectJoinedChallengeAdmin(ExportableJoinedChallengeAdmin):
    list_display = ('main_joined_challenge', 'project_name')


class ReactingJoinedChallengeAdmin(ExportableJoinedChallengeAdmin):
    list_display = ('main_joined_challenge', )


class SupportJoinedChallengeAdmin(ExportableJoinedChallengeAdmin):
    list_display = ('main_joined_challenge', )


class CustomJoinedChallengeAdmin(ExportableJoinedChallengeAdmin):
    list_display = ('main_joined_challenge', )


class QuizJoinedChallengeAdmin(ExportableJoinedChallengeAdmin):
    list_display = ('main_joined_challenge', )


class UserAnswerAdmin(ExportableJoinedChallengeAdmin):
    list_display = ('answer', 'quiz_joined_challenge')


admin.site.register(JoinedChallenge, JoinedChallengeAdmin)
admin.site.register(JoinedChallengeFile, JoinedChallengeFileAdmin)

admin.site.register(ArticleJoinedChallenge, ArticleJoinedChallengeAdmin)
admin.site.register(EventParticipantJoinedChallenge, EventParticipantJoinedChallengeAdmin)
admin.site.register(SchoolGSAJoinedChallenge, SchoolGSAJoinedChallengeAdmin)
admin.site.register(EventOrganizerJoinedChallenge, EventOrganizerJoinedChallengeAdmin)
admin.site.register(StoryJoinedChallenge, StoryJoinedChallengeAdmin)
admin.site.register(ProjectJoinedChallenge, ProjectJoinedChallengeAdmin)
admin.site.register(ReactingJoinedChallenge, ReactingJoinedChallengeAdmin)
admin.site.register(SupportJoinedChallenge, SupportJoinedChallengeAdmin)
admin.site.register(CustomJoinedChallenge, CustomJoinedChallengeAdmin)

admin.site.register(QuizJoinedChallenge, QuizJoinedChallengeAdmin)
admin.site.register(UserAnswer, UserAnswerAdmin)
