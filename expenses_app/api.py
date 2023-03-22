from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from expenses_app.models import Expenses
from expenses_app.serializers import ExpensesSerializer
from expenses_app.servise import top_cat


class ExpensesViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer


class ExpensesList(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Апи для вывода списка трат"""
    serializer_class = ExpensesSerializer

    def get_queryset(self):
        queryset = Expenses.objects.all()
        user_name = self.request.query_params.get('user') #параметр выбора пользователя
        num = self.request.query_params.get('num') # параметр выбора количества последних трат
        if user_name:
            user = User.objects.get(username=user_name)
            queryset = queryset.filter(user=user.id)
        if num:
            queryset = queryset.reverse()[:int(num)]
        return queryset

    def get(self, request):
        return self.list(request)


class TopCategory(APIView):
    """Апи для вывода популярных категорий"""

    def get(self, request):
        queryset = Expenses.objects.all()
        user_name = self.request.query_params.get('user') #параметр выбора пользователя
        num = self.request.query_params.get('num')  # параметр выбора количества категорий
        k = 15
        print(1)
        if user_name:
            user = User.objects.get(username=user_name)
            queryset = queryset.filter(user=user.id)
        if num:
            k = num
        queryset = top_cat(queryset, k)

        print(queryset)
        return Response(queryset)


class ExpensivePurchases(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Апи для вывода максимальных трат"""
    serializer_class = ExpensesSerializer

    def get_queryset(self):
        queryset = Expenses.objects.all()
        user_name = self.request.query_params.get('user')  # параметр выбора пользователя
        num = self.request.query_params.get('num')  # параметр выбора количества трат
        k = 1
        if user_name:
            user = User.objects.get(username=user_name)
            queryset = queryset.filter(user=user.id)
        if num:
            k = int(num)
        queryset = queryset.order_by('-money')[:k]
        return queryset

    def get(self, request):
        return self.list(request)
