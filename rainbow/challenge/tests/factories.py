import factory
from factory import RelatedFactory, SubFactory
from factory.django import DjangoModelFactory

from challenge.models import Challenge, ArticleChallenge
from challenge.models.base import ChallengeType


class ChallengeModelFactory(DjangoModelFactory):
    class Meta:
        model = Challenge

    points = factory.Faker('pyint', min_value=0, max_value=100)
    multiple = factory.Faker('pybool')
    needs_confirmation = factory.Faker('pybool')
    type = ChallengeType.ARTICLE


class ArticleChallengeModelFactory(DjangoModelFactory):
    class Meta:
        model = ArticleChallenge

    uuid = factory.Faker('uuid4')
    main_challenge = SubFactory(ChallengeModelFactory)
