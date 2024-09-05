from django.contrib import admin
from django import forms
from .models import Workshop, WorkshopDateTime

class WorkshopDateTimeForm(forms.ModelForm):
    class Meta:
        model = WorkshopDateTime
        fields = ['workshop', 'date_time', 'location']
        widgets = {
            'date_time': forms.SplitDateTimeWidget(
                date_attrs={'type': 'date'},
                time_attrs={'type': 'time'}
            ),
        }

class WorkshopDateTimeInline(admin.TabularInline):
    model = WorkshopDateTime
    form = WorkshopDateTimeForm
    extra = 1
    fields = ('date_time', 'location')


# WorkshopAdmin (mimicking ProductAdmin)
@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')  # Keep the same
    list_filter = ('title', 'category')  # Keep the same
    search_fields = ('title', 'description')  # Keep the same
    inlines = [WorkshopDateTimeInline]  # Include the inline

    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'price', 'category', 'duration', 'image')  # Keep the same
        }),
    )


# Register the WorkshopDateTime model with admin
admin.site.register(WorkshopDateTime)

