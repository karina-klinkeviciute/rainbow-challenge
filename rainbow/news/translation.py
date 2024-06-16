from modeltranslation.translator import TranslationOptions, translator

from news.models import NewsItem


class NewsItemTranslationOptions(TranslationOptions):
    fields = ('title', 'body', 'published')


translator.register(NewsItem, NewsItemTranslationOptions)
