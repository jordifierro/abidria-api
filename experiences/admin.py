from django.contrib import admin
from .models import ORMExperience


class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('title', )
    search_fields = ('title', 'description')


admin.site.register(ORMExperience, ExperienceAdmin)
