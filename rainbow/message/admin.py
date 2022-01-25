from django.contrib import admin

from message.models import Message


class MessageAdmin(admin.ModelAdmin):
    fields = ('user', "message_text", "admin_sender", "type", 'automated', 'time_sent', 'seen')
    list_display = ('user', "automated", "type", 'time_sent')
    list_filter = ('automated', "type", )
    readonly_fields = ('time_sent', )


admin.site.register(Message, MessageAdmin)
