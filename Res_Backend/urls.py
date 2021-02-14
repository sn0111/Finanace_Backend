from django.contrib import admin
from django.urls import path,include,re_path
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf import settings
from rest_framework.documentation import include_docs_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'^docs/',include_docs_urls(title="Finanace")),
    path('fin/',include('Receipts.urls')),
    re_path(r'^.*',views.index,name="index")
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL ,document_root = settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL ,document_root = settings.MEDIA_ROOT)
