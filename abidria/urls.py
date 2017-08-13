from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from experiences.factories import ExperiencesViewFactory
from scenes.factories import ScenesViewFactory

from .views import ViewWrapper

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^experiences/$',
        ViewWrapper.as_view(view_factory=ExperiencesViewFactory),
        name='experiences'),

    url(r'^scenes/$',
        ViewWrapper.as_view(view_factory=ScenesViewFactory),
        name='scenes'),
]

if settings.LOCAL_DEPLOY:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
