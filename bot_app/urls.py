from django.urls import path
from rest_framework import routers

from bot_app.api import AddToken, AddLimit, AddMonthLimit

router = routers.DefaultRouter()
urlpatterns = [
    path('token/', AddToken.as_view(), name='AddToken'),
    path('limit/', AddLimit.as_view(), name='AddLimit'),
    path('monthlimit/', AddMonthLimit.as_view(), name='AddLimit'),
    ]
