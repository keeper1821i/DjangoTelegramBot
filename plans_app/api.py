from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from plans_app.models import PlanExpenses


class AddPlan(APIView):
    """апи для добавления продуктов в список покупок """
    def post(self, request):
        username = request.data.get('user')
        plan = request.data.get('plan')
        category = request.data.get('category')
        if User.objects.filter(username='User' + username).exists():
            user = User.objects.get(username='User' + username)
            new_plan = PlanExpenses(product=plan,
                                    user=user,
                                    category=category)
            new_plan.save()
        else:
            return Response('такого пользователя нет', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response('test', status=status.HTTP_201_CREATED)
