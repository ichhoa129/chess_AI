from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('api/move', views.move),
    path('api/start', views.start),
    path('api/stop', views.stop),
]