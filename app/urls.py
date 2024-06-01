"""Module for urls."""
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views


router = DefaultRouter()
router.register(r'buttons', views.ButtonViewSet)
router.register(r'masters', views.MasterViewSet, basename='master')

urlpatterns = [
    path('api/', include(router.urls), name='api'),
]
