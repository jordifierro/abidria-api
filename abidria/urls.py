from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from experiences.factories import ExperiencesViewFactory
from experiences.django_views import UploadExperiencePictureView
from scenes.factories import ScenesViewFactory, SceneViewFactory
from scenes.django_views import UploadScenePictureView

from .views import ViewWrapper

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^experiences/$',
        ViewWrapper.as_view(view_factory=ExperiencesViewFactory),
        name='experiences'),

    url(r'experiences/(?P<experience_id>[0-9]+)/picture/$',
        UploadExperiencePictureView.as_view(),
        name='upload-experience-picture'),

    url(r'^scenes/$',
        ViewWrapper.as_view(view_factory=ScenesViewFactory),
        name='scenes'),

    url(r'^scenes/(?P<scene_id>[0-9]+)$',
        ViewWrapper.as_view(view_factory=SceneViewFactory),
        name='scene'),

    url(r'scenes/(?P<scene_id>[0-9]+)/picture/$',
        UploadScenePictureView.as_view(),
        name='upload-scene-picture')
]

if settings.LOCAL_DEPLOY:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
