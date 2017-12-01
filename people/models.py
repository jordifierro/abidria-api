from django.db import models


class ORMPerson(models.Model):
    is_registered = models.BooleanField(default=False)
    username = models.CharField(max_length=20, blank=True, null=True, unique=True)
    email = models.CharField(max_length=64, blank=True, null=True, unique=True)
    is_email_confirmed = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Person'
        verbose_name_plural = 'People'

    def __str__(self):
        if self.is_registered:
            return self.username
        else:
            return "anonymous_{}".format(self.id)
