from django.contrib import admin
from .models import ORMExperience, ORMSave


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', 'description')


admin.site.register(ORMExperience, ExperienceAdmin)


class SaveAdmin(admin.ModelAdmin):
    list_display = ('person', 'experience')
    search_fields = ('person', 'experience')


admin.site.register(ORMSave, SaveAdmin)
