from modeltranslation.translator import TranslationOptions, translator
from texts.models import Text

class TextTranslationOptions(TranslationOptions):
    fields = ('body', 'title', 'notes')

translator.register(Text, TextTranslationOptions)