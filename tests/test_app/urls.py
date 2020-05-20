from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

try:
    from django.conf.urls import url, include
except ImportError:
    from django.conf.urls.defaults import url, include

from . import views

urlpatterns = [
    url(r'admin/', admin.site.urls),
    url(r'make_messages/', views.make_messages, name='make_messages'),
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

if 'debug_toolbar' in settings.INSTALLED_APPS:
    try:
        import debug_toolbar

        urlpatterns.append(url(r'__debug__/', include(debug_toolbar.urls)))
    except ImportError:
        pass
