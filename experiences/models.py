from django.db import models
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID, pre_delete_delete_callback, pre_save_delete_callback

from people.models import ORMPerson


class ORMExperience(models.Model):
    title = models.CharField(max_length=30, blank=False)
    description = models.TextField(blank=True)
    picture = StdImageField(upload_to=UploadToUUID(path='experiences'),
                            variations={'large': (1280, 1280),
                                        'medium': (640, 640),
                                        'small': (320, 320)},
                            blank=True)
    author = models.ForeignKey(ORMPerson, null=True, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Experience'
        verbose_name_plural = 'Experiences'

    def __str__(self):
        return self.title


models.signals.post_delete.connect(pre_delete_delete_callback, sender=ORMExperience)
models.signals.pre_save.connect(pre_save_delete_callback, sender=ORMExperience)


class ORMSave(models.Model):
    person = models.ForeignKey(ORMPerson, on_delete=models.CASCADE)
    experience = models.ForeignKey(ORMExperience, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Save'
        verbose_name_plural = 'Saves'

    def __str__(self):
        return "{} - {}".format(str(self.person), str(self.experience))
