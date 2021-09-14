from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView, TemplateView, FormView

from challenge.forms.article import ArticleChallengeForm
from challenge.forms.event_participant import EventParticipantChallengeForm
from challenge.models import ArticleChallenge


@method_decorator(staff_member_required, name='dispatch')
class ArticleChallengeListView(ListView):
    model = ArticleChallenge
    template_name = 'challenge/challenge-list.html'


class BaseChallengeView(TemplateView):
    template_name = 'challenge/challenge.html'

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        uuid = kwargs.get('uuid')
        if uuid is not None:
            instance = self.challenge_model.objects.get(pk=uuid)
            form = self.form(instance=instance.main_challenge)
            context["view"].form = form
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        context = self.get_context_data()
        form = context["view"].form
        uuid = kwargs.get('uuid')
        if uuid is not None:
            article_challenge = self.challenge_model.objects.get(pk=uuid)
            challenge = article_challenge.main_challenge
            form = form(request.POST, instance=challenge)
        if form.is_valid():
            instance = form.save()
            instance.save()
            context["view"].form = form

        return self.render_to_response(context)


@method_decorator(staff_member_required, name='dispatch')
class ArticleChallengeView(BaseChallengeView):
    form = ArticleChallengeForm
    challenge_model = ArticleChallenge


@method_decorator(staff_member_required, name='dispatch')
class EventParticipantChallengeView(View):
    template_name = 'challenge/challenge.html'
    form = EventParticipantChallengeForm
