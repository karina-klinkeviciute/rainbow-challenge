from django.contrib import admin

from joined_challenge.models import JoinedChallenge, ArticleJoinedChallenge, EventParticipantJoinedChallenge, \
    SchoolGSAJoinedChallenge, EventOrganizerJoinedChallenge, StoryJoinedChallenge, ProjectJoinedChallenge, \
    ReactingJoinedChallenge, SupportJoinedChallenge, CustomJoinedChallenge, QuizJoinedChallenge


class JoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'status')

class ArticleJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', 'article_name', 'article_url')

class EventParticipantJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', )

class SchoolGSAJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', )

class EventOrganizerJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', 'event_name')

class StoryJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', )

class ProjectJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', 'project_name')

class ReactingJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', )

class SupportJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', )

class CustomJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', )

class QuizJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', )

admin.site.register(JoinedChallenge, JoinedChallengeAdmin)

# joined challenge
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
