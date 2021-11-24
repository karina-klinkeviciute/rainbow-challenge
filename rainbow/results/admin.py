from django.contrib import admin

# Register your models here.
from results.models import Medal
from results.models.prize import Prize, ClaimedPrize
from results.models.region import Region


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name', )

class PrizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'amount', )

class ClaimedPrizeAdmin(admin.ModelAdmin):
    list_display = ('prize', 'user', 'amount', 'issued')
    list_filter = ('prize', 'user', 'issued')

class MedalAdmin(admin.ModelAdmin):
    list_display = ('user', 'level')


admin.site.register(Region, RegionAdmin)
admin.site.register(Prize, PrizeAdmin)
admin.site.register(ClaimedPrize, ClaimedPrizeAdmin)
admin.site.register(Medal, MedalAdmin)
