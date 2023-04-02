from rest_framework import serializers

from bot_app.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['user', 'external_id', 'name', 'token']