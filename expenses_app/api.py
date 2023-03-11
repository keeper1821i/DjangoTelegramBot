from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from expenses_app.models import Expenses
from expenses_app.serializers import ExpensesSerializer



class ExpensesViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer


class ExpensesList(ListModelMixin, CreateModelMixin, GenericAPIView):
    serializer_class = ExpensesSerializer

    def get_queryset(self):
        queryset = Expenses.objects.all()
        user_name = self.request.query_params.get('user')
        if user_name:
            user = User.objects.get(username=user_name)
            queryset = queryset.filter(user=user.id)
        return queryset
    def get(self, request):
        return self.list(request)

    def post(self, request, format=None):
        return self.create(request)


