from django.urls import path
from rest_framework import routers
from expenses_app.api import ExpensesViewSet, ExpensesList, TopCategory, ExpensivePurchases


router = routers.DefaultRouter()
urlpatterns = [
    path('exp/', ExpensesList.as_view(), name='ExpensesList'),
    path('cat/', TopCategory.as_view(), name='TopCategory'),
    path('max/', ExpensivePurchases.as_view()),
    path('total_exp/', ExpensesViewSet.as_view())
    ]
