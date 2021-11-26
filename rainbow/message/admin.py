from django.contrib import admin

from message.models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', "automated", "type", )
    list_filter = ('automated', "type", )


admin.site.register(Message, MessageAdmin)
