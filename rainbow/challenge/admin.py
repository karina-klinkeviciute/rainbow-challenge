from django.contrib import admin

from challenge.models import Challenge, ArticleChallenge, EventParticipantChallenge, JoinedChallenge, \
    ArticleJoinedChallenge, EventParticipantJoinedChallenge, Region


# Challenges

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


admin.site.register(Challenge, ChallengeAdmin)
admin.site.register(ArticleChallenge, ArticleChallengeAdmin)
admin.site.register(EventParticipantChallenge, EventParticipantChallengeAdmin)
admin.site.register(JoinedChallenge, JoinedChallengeAdmin)
admin.site.register(ArticleJoinedChallenge, ArticleJoinedChallengeAdmin)
admin.site.register(EventParticipantJoinedChallenge, EventParticipantJoinedChallengeAdmin)
admin.site.register(Region, RegionAdmin)
