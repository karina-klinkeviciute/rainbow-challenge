import qrcode
from django.conf import settings
from django.contrib import admin
from django.core.files import File

from django.utils.translation import gettext_lazy as _

from challenge.models import Challenge, ArticleChallenge, EventParticipantChallenge, SupportChallenge, QuizChallenge, \
    CustomChallenge

from challenge.models.event_organizer import EventOrganizerChallenge
from challenge.models.project import ProjectChallenge
from challenge.models.reacting import ReactingChallenge
from challenge.models.school_gsa import SchoolGSAChallenge
from challenge.models.story import StoryChallenge


@admin.action(description=_('Generate QR code files'))
def generate_qr_codes(modeladmin, request, queryset):
    for event_challenge in queryset:
        if event_challenge.qr_code_file.name == '':
            if event_challenge.qr_code is not None:
                image = qrcode.make(event_challenge.qr_code)
                file_name = f"{settings.MEDIA_ROOT}/qrcodes/{event_challenge.qr_code}.png"
                django_file_name = f"{event_challenge.qr_code}.png"
                image.save(file_name)
                with open(file_name, "rb") as reopen:
                    djangofile = File(reopen)
                    event_challenge.qr_code_file.save(django_file_name, djangofile)


class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'type', 'points', 'region', 'published', 'start_date', 'end_date')
    list_filter = ('type', 'region', 'published', )

class ArticleChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_challenge', )

class EventParticipantChallengeAdmin(admin.ModelAdmin):
    list_display = ('event_name', )
    actions = [generate_qr_codes]

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

class SupportChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_challenge', 'organization', )

class QuizChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_challenge', 'quiz', )

class CustomChallengeAdmin(admin.ModelAdmin):
    list_display = ('main_challenge', )


admin.site.register(Challenge, ChallengeAdmin)


admin.site.register(ArticleChallenge, ArticleChallengeAdmin)
admin.site.register(EventParticipantChallenge, EventParticipantChallengeAdmin)
admin.site.register(SchoolGSAChallenge, SchoolGSAChallengeAdmin)
admin.site.register(EventOrganizerChallenge, EventOrganizerChallengeAdmin)
admin.site.register(StoryChallenge, StoryChallengeAdmin)
admin.site.register(ProjectChallenge, ProjectChallengeAdmin)
admin.site.register(ReactingChallenge, ReactingChallengeAdmin)
admin.site.register(SupportChallenge, SupportChallengeAdmin)
admin.site.register(QuizChallenge, QuizChallengeAdmin)
admin.site.register(CustomChallenge, CustomChallengeAdmin)
