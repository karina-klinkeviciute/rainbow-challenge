from django.contrib import admin

from challenge.models import Challenge, ArticleChallenge, EventParticipantChallenge, JoinedChallenge, \
    ArticleJoinedChallenge, EventParticipantJoinedChallenge, Region, Prize


# Challenges
from challenge.models.prize import ClaimedPrize


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'type', 'points', 'region')

class ArticleChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_challenge', )

class EventParticipantChallengeAdmin(admin.ModelAdmin):
    list_display = ('event_name', )

#     Joined challenges

class JoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('user', 'challenge', 'status')

class ArticleJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', 'article_name', 'article_url')

class EventParticipantJoinedChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_joined_challenge', )

class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', )

class PrizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount')

class ClaimedPrizeAdmin(admin.ModelAdmin):
    list_display = ('prize', 'user', 'amount', 'issued')
    list_filter = ('prize', 'user', 'issued')

admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(ArticleChallenge, ArticleChallengeAdmin)
admin.site.register(EventParticipantChallenge, EventParticipantChallengeAdmin)
admin.site.register(JoinedChallenge, JoinedChallengeAdmin)
admin.site.register(ArticleJoinedChallenge, ArticleJoinedChallengeAdmin)
admin.site.register(EventParticipantJoinedChallenge, EventParticipantJoinedChallengeAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Prize, PrizeAdmin)
admin.site.register(ClaimedPrize, ClaimedPrizeAdmin)
