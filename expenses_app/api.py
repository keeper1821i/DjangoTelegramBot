from django.contrib.auth.models import User
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from expenses_app.models import Expenses
from expenses_app.serializers import ExpensesSerializer
from expenses_app.servise import top_cat, check_token


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
        token = self.request.query_params.get('token') # токен для проверки авторизации
        if check_token(token, user_name):
            if user_name:
                user = User.objects.get(username='User' + user_name)
                queryset = queryset.filter(user=user.id)
            if num:
                queryset = queryset.reverse()[:int(num)]
            return queryset
        else:
            return Response('Не верный токен', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        return self.list(request)


class TopCategory(APIView):
    """Апи для вывода популярных категорий"""

    def get(self, request):
        queryset = Expenses.objects.all()
        user_name = self.request.query_params.get('user') #параметр выбора пользователя
        num = self.request.query_params.get('num')  # параметр выбора количества категорий
        k = 15
        token = self.request.query_params.get('token')  # токен для проверки авторизации
        if check_token(token, user_name):
            if user_name:
                user = User.objects.get(username='User' + user_name)
                queryset = queryset.filter(user=user.id)
            if num:
                k = num
            queryset = top_cat(queryset, k)
            return Response(queryset)
        else:
            return Response('Не верный токен', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ExpensivePurchases(ListModelMixin, CreateModelMixin, GenericAPIView):
    """Апи для вывода максимальных трат"""
    serializer_class = ExpensesSerializer

    def get_queryset(self):
        queryset = Expenses.objects.all()
        user_name = self.request.query_params.get('user')  # параметр выбора пользователя
        num = self.request.query_params.get('num')  # параметр выбора количества трат
        k = 1
        token = self.request.query_params.get('token')  # токен для проверки авторизации
        if check_token(token, user_name):
            if user_name:
                user = User.objects.get(username='User' + user_name)
                queryset = queryset.filter(user=user.id)
            if num:
                k = int(num)
            queryset = queryset.order_by('-money')[:k]
            return queryset
        else:
            return Response('Не верный токен', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        return self.list(request)
