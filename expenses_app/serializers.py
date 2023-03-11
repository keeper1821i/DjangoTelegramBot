from expenses_app.models import Expenses
from rest_framework import serializers


class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expenses
        fields = ['category', 'money', 'created', 'product', 'user']
