from django.db import models
from django.utils.translation import gettext_lazy as _

from joined_challenge.models.base import BaseJoinedChallenge


class ProjectJoinedChallenge(BaseJoinedChallenge):
    project_name = models.TextField(
        verbose_name=_("name of the event"),
        blank=True,
        null=True
    )
    project_url = models.URLField(
        verbose_name=_('link to the event website or Facebook page if there is one'),
        blank=True,
        null=True
    )
    description = models.TextField(
        verbose_name=_('description of the event in your own words'),
        blank=True,
        null=True
    )
    implemented_alone = models.BooleanField(
        verbose_name=_('if this project was implemented by you alone'),
        blank=True,
        null=True
    )

    @property
    def concrete_challenge(self):
        from challenge.models.project import ProjectChallenge
        return ProjectChallenge.objects.get(main_challenge=self.main_joined_challenge.challenge)
