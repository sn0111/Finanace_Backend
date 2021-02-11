from django.contrib import admin
from django.urls import path,include
# from res.urls import *
urlpatterns = [
    path('admin/', admin.site.urls),
    path('fin/',include('Receipts.urls')),
]
