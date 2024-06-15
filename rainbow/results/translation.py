from modeltranslation.translator import TranslationOptions, translator

from results.models import Prize


class PrizeTranslationOptions(TranslationOptions):
    fields = ('name', 'description', 'available')


translator.register(Prize, PrizeTranslationOptions)
