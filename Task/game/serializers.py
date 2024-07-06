from rest_framework import serializers
from .models import *

class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = GameSession
        fields = ['id', 'credits']


class GameSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'account_credits']
