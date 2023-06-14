from django.urls import path
from rest_framework import routers

from plans_app.api import AddPlan

router = routers.DefaultRouter()
urlpatterns = [
    path('plan/', AddPlan.as_view(), name='AddPlan'),
    ]
