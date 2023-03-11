from django.urls import path
from rest_framework import routers
from expenses_app.api import ExpensesViewSet, ExpensesList


router = routers.DefaultRouter()
router.register('expenses', ExpensesViewSet)
urlpatterns = [
    # router.urls,
    path('exp/', ExpensesList.as_view(), name='ExpensesList')
    ]
