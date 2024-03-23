from rest_framework import serializers
# from ..models.user import User
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username',  'email' ]
