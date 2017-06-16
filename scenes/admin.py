from django.contrib import admin
from .models import ORMScene


class SceneAdmin(admin.ModelAdmin):
    list_display = ('title', 'experience')
    search_fields = ('title', 'description')


admin.site.register(ORMScene, SceneAdmin)
