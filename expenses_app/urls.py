from django.urls import path
from rest_framework import routers
from expenses_app.api import ExpensesViewSet, ExpensesList, TopCategory, ExpensivePurchases


router = routers.DefaultRouter()
router.register('expenses', ExpensesViewSet)
urlpatterns = [
    path('exp/', ExpensesList.as_view(), name='ExpensesList'),
    path('cat/', TopCategory.as_view(), name='TopCategory'),
    path('max/', ExpensivePurchases.as_view())
    ]
