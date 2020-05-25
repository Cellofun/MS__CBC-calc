from django.contrib import admin

from .models import CompleteBloodCount, ThreeDiff, FiveDiff, BloodSmear


class CompleteBloodCountAdmin(admin.ModelAdmin):
    exclude = ['type', 'sum']


admin.site.register(CompleteBloodCount, CompleteBloodCountAdmin)
admin.site.register(ThreeDiff)
admin.site.register(FiveDiff)
admin.site.register(BloodSmear)
