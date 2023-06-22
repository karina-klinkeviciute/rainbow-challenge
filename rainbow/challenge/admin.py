import qrcode
from django.conf import settings
from django.contrib import admin
from django.contrib.admin import display
from django.core.files import File

from django.utils.translation import gettext_lazy as _
from fcm_django.models import FCMDevice
from import_export.admin import ExportMixin
from nested_inline.admin import NestedStackedInline, NestedModelAdmin
from firebase_admin.messaging import Message as PushNotification, Notification

from challenge.models import Challenge, ArticleChallenge, EventParticipantChallenge, SupportChallenge, QuizChallenge, \
    CustomChallenge

from challenge.models.event_organizer import EventOrganizerChallenge
from challenge.models.project import ProjectChallenge
from challenge.models.quiz import Answer, Question
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

@admin.action(description=_('Send push notifications'))
def send_push_notification(modeladmin, request, queryset):
    for concrete_challenge in queryset:
        message_text = _(
            f"New challenge added: "
        ) + concrete_challenge.challenge.name

        devices = FCMDevice.objects.all()
        notification = PushNotification(
            notification=Notification(title=_("New challenge added"), body=message_text)
        )
        devices.send_message(notification)

class ChallengeAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('name', 'description', 'image', 'type', 'points', 'region', 'published', 'start_date', 'end_date')
    list_filter = ('type', 'region', 'published', )


class BaseChallengeAdmin(ExportMixin, admin.ModelAdmin):
    list_display = ('main_challenge', 'get_published')

    @display(ordering='main_challenge__published', description='Published')
    def get_published(self, obj):
        return obj.main_challenge.published


class ArticleChallengeAdmin(BaseChallengeAdmin):
    pass


class EventParticipantChallengeAdmin(BaseChallengeAdmin):
    list_display = ('event_name', 'get_published')
    actions = [generate_qr_codes]


class SchoolGSAChallengeAdmin(BaseChallengeAdmin):
    pass


class EventOrganizerChallengeAdmin(BaseChallengeAdmin):
    pass


class StoryChallengeAdmin(BaseChallengeAdmin):
    pass


class ProjectChallengeAdmin(BaseChallengeAdmin):
    pass


class ReactingChallengeAdmin(BaseChallengeAdmin):
    pass


class SupportChallengeAdmin(BaseChallengeAdmin):
    list_display = ('main_challenge', 'organization', 'get_published')


class CustomChallengeAdmin(BaseChallengeAdmin):
    pass


class AnswerInline(NestedStackedInline):
    model = Answer
    extra = 1
    fk_name = 'question'


class QuestionInline(NestedStackedInline):
    model = Question
    extra = 1
    fk_name = 'quiz'
    inlines = (AnswerInline, )


class QuizChallengeAdmin(NestedModelAdmin, BaseChallengeAdmin):
    list_display = ('main_challenge', 'get_published')
    inlines = (QuestionInline, )


admin.site.register(Challenge, ChallengeAdmin)


admin.site.register(ArticleChallenge, ArticleChallengeAdmin)
admin.site.register(EventParticipantChallenge, EventParticipantChallengeAdmin)
admin.site.register(SchoolGSAChallenge, SchoolGSAChallengeAdmin)
admin.site.register(EventOrganizerChallenge, EventOrganizerChallengeAdmin)
admin.site.register(StoryChallenge, StoryChallengeAdmin)
admin.site.register(ProjectChallenge, ProjectChallengeAdmin)
admin.site.register(ReactingChallenge, ReactingChallengeAdmin)
admin.site.register(SupportChallenge, SupportChallengeAdmin)

admin.site.register(CustomChallenge, CustomChallengeAdmin)

admin.site.register(QuizChallenge, QuizChallengeAdmin)
