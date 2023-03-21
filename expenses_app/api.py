from django.contrib.auth.models import User
from django.db.models import Max, F
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from expenses_app.models import Expenses
from expenses_app.serializers import ExpensesSerializer
from expenses_app.servise import top_cat, max_ex


class ExpensesViewSet(viewsets.ModelViewSet):
    queryset = Expenses.objects.all()
    serializer_class = ExpensesSerializer


class ExpensesList(ListModelMixin, CreateModelMixin, GenericAPIView):
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



# class ExpensivePurchases(ListModelMixin, CreateModelMixin, GenericAPIView):
#     serializer_class = ExpensesSerializer
#
#     def get_queryset(self):
#         queryset = Expenses.objects.annotate(max_money=Max('money')).filter(money=F('max_money')).first()
#         user_name = self.request.query_params.get('user')  # параметр выбора пользователя
#         num = self.request.query_params.get('num')  # параметр выбора количества категорий
#         k = 1
#         if user_name:
#             user = User.objects.get(username=user_name)
#             queryset = queryset.filter(user=user.id)
#         if num:
#             k = num
#         for _ in range(k):
#             print(Expenses.objects.annotate(max_money=Max('money')).filter(money=F('max_money')).first())
#         return queryset
#
#     def get(self, request):
#         return self.list(request)
