from django.urls import path
from res.views import *
urlpatterns =[
    path("main",main),
    path("register",Register.as_view()),
]