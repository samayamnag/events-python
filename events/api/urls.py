from django.urls import path
from .views import EventDetail,CreateEvent
from rest_framework.routers import DefaultRouter


app_name = 'events'

urlpatterns = [
    path('create', CreateEvent.as_view(), name="create-events"),
    path('<str:id>', EventDetail.as_view(), name="rud-events")
]