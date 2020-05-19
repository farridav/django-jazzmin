from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('make_messages/', views.make_messages, name='make_messages'),
]

if settings.DEBUG:
    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))

if 'debug_toolbar' in settings.INSTALLED_APPS:
    try:
        import debug_toolbar

        urlpatterns.append(path('__debug__/', include(debug_toolbar.urls)))
    except ImportError:
        pass
