# from modeltranslation.translator import TranslationOptions, translator
#
# from challenge.models import EventParticipantChallenge, SupportChallenge
# from challenge.models.base import Topic, Challenge
#
#
# class TopicTranslationOptions(TranslationOptions):
#     fields = ('topic', )
#
# class ChallengeTranslationOptions(TranslationOptions):
#     fields = ('_name', 'description', 'published')
#
# class EventParticipantChallengeTranslationOptions(TranslationOptions):
#     fields = ('event_name', )
#
# class SupportChallengeTranslationOptions(TranslationOptions):
#     fields = ('organization', )
#
# translator.register(Topic, TopicTranslationOptions)
# translator.register(Challenge, ChallengeTranslationOptions)
# translator.register(EventParticipantChallenge, EventParticipantChallengeTranslationOptions)
# translator.register(SupportChallenge, SupportChallengeTranslationOptions)
