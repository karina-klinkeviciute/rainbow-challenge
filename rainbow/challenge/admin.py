from django.contrib import admin

from challenge.models import Challenge, ArticleChallenge, EventParticipantChallenge, JoinedChallenge, \
    ArticleJoinedChallenge, EventParticipantJoinedChallenge, Region, Prize, EventOrganizerJoinedChallenge

from challenge.models.challenge.event_organizer import EventOrganizerChallenge
from challenge.models.challenge.project import ProjectChallenge
from challenge.models.challenge.reacting import ReactingChallenge
from challenge.models.challenge.school_gsa import SchoolGSAChallenge
from challenge.models.challenge.story import StoryChallenge
from challenge.models.joined_challenge.project import ProjectJoinedChallenge
from challenge.models.joined_challenge.reacting import ReactingJoinedChallenge
from challenge.models.joined_challenge.school_gsa import SchoolGSAJoinedChallenge
from challenge.models.joined_challenge.story import StoryJoinedChallenge
from challenge.models.prize import ClaimedPrize

# Challenges
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type', 'points', 'region', 'published', 'start_date', 'end_date')
    list_filter = ('type', 'region', 'published', )

class ArticleChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_challenge', )

class EventParticipantChallengeAdmin(admin.ModelAdmin):
    list_display = ('event_name', )

class SchoolGSAChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_challenge', )

class EventOrganizerChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_challenge', )

class StoryChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_challenge', )

class ProjectChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_challenge', )

class ReactingChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_challenge', )

#     Joined challenges

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
    list_display = ('main_joined_challenge', 'project_name')


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', )

class PrizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')

class ClaimedPrizeAdmin(admin.ModelAdmin):
    list_display = ('prize', 'user', 'amount', 'issued')
    list_filter = ('prize', 'user', 'issued')

admin.site.register(Challenge, ChallengeAdmin)

# challenge
admin.site.register(ArticleChallenge, ArticleChallengeAdmin)
admin.site.register(EventParticipantChallenge, EventParticipantChallengeAdmin)
admin.site.register(SchoolGSAChallenge, SchoolGSAChallengeAdmin)
admin.site.register(EventOrganizerChallenge, EventOrganizerChallengeAdmin)
admin.site.register(StoryChallenge, StoryChallengeAdmin)
admin.site.register(ProjectChallenge, ProjectChallengeAdmin)
admin.site.register(ReactingChallenge, ReactingChallengeAdmin)

admin.site.register(JoinedChallenge, JoinedChallengeAdmin)

# joined challenge
admin.site.register(ArticleJoinedChallenge, ArticleJoinedChallengeAdmin)
admin.site.register(EventParticipantJoinedChallenge, EventParticipantJoinedChallengeAdmin)
admin.site.register(SchoolGSAJoinedChallenge, SchoolGSAJoinedChallengeAdmin)
admin.site.register(EventOrganizerJoinedChallenge, EventOrganizerJoinedChallengeAdmin)
admin.site.register(StoryJoinedChallenge, StoryJoinedChallengeAdmin)
admin.site.register(ProjectJoinedChallenge, ProjectJoinedChallengeAdmin)
admin.site.register(ReactingJoinedChallenge, ReactingJoinedChallengeAdmin)

admin.site.register(Region, RegionAdmin)
admin.site.register(Prize, PrizeAdmin)
admin.site.register(ClaimedPrize, ClaimedPrizeAdmin)
