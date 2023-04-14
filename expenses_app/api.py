from django.contrib.auth.models import User

from rest_framework import viewsets, status
from rest_framework.filters import OrderingFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView, ListAPIView
from rest_framework.views import APIView
from expenses_app.models import Expenses
from expenses_app.serializers import ExpensesSerializer
from expenses_app.servise import top_cat, check_token


class StandardResultsSetPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    max_page_size = 1000


class ExpensesViewSet(ListAPIView):
    serializer_class = ExpensesSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['category', 'money', 'created']

    def get_queryset(self):
        queryset = Expenses.objects.all()
        user_name = self.request.query_params.get('user')  # параметр выбора пользователя
        token = self.request.query_params.get('token')  # токен для проверки авторизации
        date_start = self.request.query_params.get('date_start')
        date_end = self.request.query_params.get('date_end')
        if check_token(token, user_name):
            if user_name:
                user = User.objects.get(username='User' + user_name)
                queryset = queryset.filter(user=user.id)
            if date_start:
                queryset = queryset.filter(created__gt=date_start)
            if date_end:
                queryset = queryset.filter(created__lt=date_end)
            return queryset
        else:
            return Response('Не верный токен', status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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
