from django.urls import path
from rest_framework import routers

from bot_app.api import AddToken

router = routers.DefaultRouter()
urlpatterns = [
    path('token/', AddToken.as_view(), name='AddToken'),
    ]
