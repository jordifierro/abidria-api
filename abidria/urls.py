from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from experiences.views import ExperiencesView
from experiences.factories import ExperiencesViewInjector
from scenes.views import ScenesView
from scenes.factories import ScenesViewInjector

from .views import ViewWrapper

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^experiences/$',
        ViewWrapper.as_view(view=ExperiencesView, injector=ExperiencesViewInjector),
        name='experiences'),

    url(r'^scenes/$',
        ViewWrapper.as_view(view=ScenesView, injector=ScenesViewInjector),
        name='scenes'),
]

if settings.LOCAL_DEPLOY:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
