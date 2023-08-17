from rest_framework import serializers
from .models import User,API

class UserSerializer(serializers.ModelSerializer):
   class Meta:
      model = User
      fields = '__all__'

class APISerializer(serializers.ModelSerializer):
   class Meta:
      model = API
      fields = "__all__"
      