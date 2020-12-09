from rest_framework import serializers
from .models import Post, Like, UnLike
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        lower_email = value.lower()
        if User.objects.filter(email__iexact=lower_email).exists():
            raise serializers.ValidationError("Email address is already registered")
        return lower_email


    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['id', 'text']


class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = ['post']


class UnLikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = UnLike
        fields = ['post']

