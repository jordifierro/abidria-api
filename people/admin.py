from django.contrib import admin
from .models import ORMPerson, ORMAuthToken


class PersonAdmin(admin.ModelAdmin):
    list_display = ('id', 'is_registered', 'username', 'email', 'is_email_confirmed')
    search_fields = ('username', 'email')


admin.site.register(ORMPerson, PersonAdmin)


class AuthTokenAdmin(admin.ModelAdmin):
    list_display = ('person', 'access_token', 'refresh_token')
    search_fields = ('person__username', )


admin.site.register(ORMAuthToken, AuthTokenAdmin)
