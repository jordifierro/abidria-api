from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from experiences.factories import create_experiences_view, create_experience_view
from experiences.django_views import UploadExperiencePictureView
from scenes.factories import create_scenes_view, create_scene_view
from scenes.django_views import UploadScenePictureView
from people.factories import create_people_view, create_person_view, create_email_confirmation_view

from .views import ViewWrapper

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^experiences/$',
        ViewWrapper.as_view(view_creator_func=create_experiences_view),
        name='experiences'),

    url(r'^experiences/(?P<experience_id>[0-9]+)$',
        ViewWrapper.as_view(view_creator_func=create_experience_view),
        name='experience'),

    url(r'experiences/(?P<experience_id>[0-9]+)/picture/$',
        UploadExperiencePictureView.as_view(),
        name='upload-experience-picture'),

    url(r'^scenes/$',
        ViewWrapper.as_view(view_creator_func=create_scenes_view),
        name='scenes'),

    url(r'^scenes/(?P<scene_id>[0-9]+)$',
        ViewWrapper.as_view(view_creator_func=create_scene_view),
        name='scene'),

    url(r'scenes/(?P<scene_id>[0-9]+)/picture/$',
        UploadScenePictureView.as_view(),
        name='upload-scene-picture'),

    url(r'^people/$',
        ViewWrapper.as_view(view_creator_func=create_people_view),
        name='people'),

    url(r'^people/me$',
        ViewWrapper.as_view(view_creator_func=create_person_view),
        name='person'),

    url(r'^people/me/email-confirmation$',
        ViewWrapper.as_view(view_creator_func=create_email_confirmation_view),
        name='email-confirmation'),
]

if settings.LOCAL_DEPLOY:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
