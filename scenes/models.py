from django.db import models
from stdimage.models import StdImageField
from stdimage.utils import UploadToUUID, pre_delete_delete_callback, pre_save_delete_callback

from experiences.models import ORMExperience


class ORMScene(models.Model):
    title = models.CharField(max_length=30, blank=False)
    description = models.TextField(blank=True)
    picture = StdImageField(upload_to=UploadToUUID(path='scenes'),
                            variations={'large': (1280, 1280),
                                        'medium': (640, 640),
                                        'small': (320, 320)},
                            blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    experience = models.ForeignKey(ORMExperience, on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Scene'
        verbose_name_plural = 'Scenes'

    def __str__(self):
        return self.title


models.signals.post_delete.connect(pre_delete_delete_callback, sender=ORMScene)
models.signals.pre_save.connect(pre_save_delete_callback, sender=ORMScene)
