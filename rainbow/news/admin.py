from django.contrib import admin

from news.models import NewsItem


class NewsItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'published')
    list_filter = ('published', )


admin.site.register(NewsItem, NewsItemAdmin)
