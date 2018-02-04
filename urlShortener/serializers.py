from rest_framework import serializers
from models import User, URL

class UserSerializer(serializers.ModelSerializer):
    class Meta:
	model = User
	fields = ('email', 'password')

class UrlSerializer(serializers.ModelSerializer):
    class Meta:
	model = URL
	fields = ('original', 'shortenURL', 'isActive')