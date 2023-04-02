from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from bot_app.models import Profile
from bot_app.serializers import ProfileSerializer


class AddToken(APIView):

    def post(self, request):
        queryset = Profile.objects.all()
        username = request.data.get('user')
        token = request.data.get('token')
        if User.objects.filter(username='User' + username).exists():
            user = User.objects.get(username='User' + username)
            profile = queryset.get(user=user.id)
            profile.token = token
            profile.save()
            print(token)
        else:
            return Response('такого пользователя нет', status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response('test', status=status.HTTP_201_CREATED)
