from django.contrib import admin
from .models import Workshop, WorkshopDateTime

class WorkshopDateTimeInline(admin.TabularInline):
    model = WorkshopDateTime
    extra = 1
    fields = ('date_time', 'time_choice')

@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'price')  # Date added to list
    list_filter = ('date', 'category')  # Date added to list filter
    search_fields = ('title', 'description')
    inlines = [WorkshopDateTimeInline]  # Inline formet for WorkshopDateTime

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'price', 'category', 'duration', 'image')
        }),
    )

admin.site.register(WorkshopDateTime)