from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^silk/', include('silk.urls', namespace='silk')),
    path('', TemplateView.as_view(template_name='index.html'), name='index'),
    path('account/', include('account.urls')),
    path('rate/', include('rate.urls')),
    path('password/', include('django.contrib.auth.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns.extend([
        path('__debug__/', include(debug_toolbar.urls)),
    ])
    urlpatterns.extend(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))
    urlpatterns.extend(static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT))
