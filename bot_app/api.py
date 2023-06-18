from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bot_app.models import Profile


class AddToken(APIView):
    """апи для получения токена пользователя"""
    def post(self, request):
        queryset = Profile.objects.all()
        username = request.data.get('user')
        token = request.data.get('token')
        if User.objects.filter(username='User' + username).exists():
            user = User.objects.get(username='User' + username)
            profile = queryset.get(user=user.id)
            profile.token = token
            profile.save()
        else:
            return Response('такого пользователя нет', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response('test', status=status.HTTP_201_CREATED)


class AddLimit(APIView):
    """апи для установления лимита трат """
    def post(self, request):
        queryset = Profile.objects.all()
        username = request.data.get('user')
        day_limit = request.data.get('day_limit')
        month_limit = request.data.get('month_limit')
        day_text = request.data.get('day_text')
        month_text = request.data.get('month_text')
        if User.objects.filter(username='User' + username).exists():
            user = User.objects.get(username='User' + username)
            profile = queryset.get(user=user.id)
            profile.limit = int(day_limit)
            profile.month_limit = int(month_limit)
            profile.day_text = day_text
            profile.month_text = month_text
            profile.save()
        else:
            return Response('такого пользователя нет', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response('test', status=status.HTTP_201_CREATED)

    def get(self, request):
        username = request.query_params.get('user')
        queryset = Profile.objects.filter(external_id=username).values('limit', 'day_text', 'month_limit', 'month_text')
        return Response(queryset)
