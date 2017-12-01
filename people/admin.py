from django.contrib import admin
from .models import ORMPerson


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_registered', 'username', 'email', 'is_email_confirmed')
    search_fields = ('username', 'email')


admin.site.register(ORMPerson, PersonAdmin)
