from django.contrib import admin
from .models import Record, BestRecord


# Register your models here.

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('player', 'difficulty', 'finish_time', 'create_time')


@admin.register(BestRecord)
class RecordAdmin(admin.ModelAdmin):
    list_display = ('player', 'difficulty', 'finish_time', 'create_time')