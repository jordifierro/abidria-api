from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from experiences.views import ExperiencesView, ExperienceDetailView
from scenes.views import ScenesView

from .views import ViewWrapper

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^experiences/$', ViewWrapper.as_view(view=ExperiencesView), name='experiences'),
    url(r'^experiences/(?P<id>\d+)$', ViewWrapper.as_view(view=ExperienceDetailView), name='experience-detail'),

    url(r'^scenes/$', ViewWrapper.as_view(view=ScenesView), name='scenes'),
]

if settings.LOCAL_DEPLOY:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
