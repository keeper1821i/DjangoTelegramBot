from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from plans_app.models import PlanExpenses
from expenses_app.servise import check_token

class AddPlan(APIView):
    """апи для добавления продуктов в список покупок """
    def post(self, request):
        username = request.data.get('user')
        plan = request.data.get('plan')
        category = request.data.get('category')
        date = request.data.get('date')
        token = request.data.get('token')
        if check_token(token, username):
            if User.objects.filter(username='User' + username).exists():
                user = User.objects.get(username='User' + username)
                new_plan = PlanExpenses(product=plan,
                                        user=user,
                                        category=category,
                                        created=date[:10])
                new_plan.save()
            else:
                return Response('такого пользователя нет', status=status.HTTP_408_REQUEST_TIMEOUT)
            return Response('test', status=status.HTTP_201_CREATED)
        else:
            return Response('Не верный токен', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        queryset = PlanExpenses.objects.all()
        username = request.query_params.get('user')
        token = request.query_params.get('token')
        if check_token(token, username):
            user = User.objects.get(username='User' + username)
            queryset = queryset.filter(user=user.id).values('id', 'product', 'category', 'created')
            return Response(queryset)
        else:
            return Response('Не верный токен', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        id = request.data.get('id')
        username = request.data.get('user')
        plan = request.data.get('plan')
        category = request.data.get('category')
        date = request.data.get('date')
        token = request.data.get('token')
        if check_token(token, username):
            user = User.objects.get(username='User' + username)
            PlanExpenses.objects.filter(id=int(id)).update(product=plan,
                                                           user=user,
                                                           category=category,
                                                           created=date)

            return Response('test', status=status.HTTP_200_OK)
        else:
            return Response('Не верный токен', status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        id = request.data.get('id')
        username = request.data.get('user')
        token = request.data.get('token')
        if check_token(token, username):
            user = User.objects.get(username='User' + username)
            PlanExpenses.objects.filter(id=int(id)).delete()

            return Response('test', status=status.HTTP_200_OK)
        else:
            return Response('Не верный токен', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
