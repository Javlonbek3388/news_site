from django.core.validators import FileExtensionValidator
from rest_framework import serializers
from .models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer, TokenObtainPairSerializer, TokenObtainSerializer
)
from django.db import models

from django.contrib.auth.models import update_last_login
from rest_framework.generics import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import AccessToken


class RegisterSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def validate(self, attrs):
        if attrs["password1"] != attrs["password2"]:
            raise ValidationError({"password": "Password fields didn't match."})

        return attrs

    def validate_username(self, username):
        if User.objects.filter(username=username).exists():
            data = {"status": False, "message": "Bu username mavjud"}
            raise ValidationError(data)
        return username

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            # email=validated_data['email'],
        )

        user.set_password(validated_data["password1"])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if not username or not password:
            raise serializers.ValidationError("Both username and password are required")

        return data


class UpdateAccessSerializer(TokenRefreshSerializer):
    def validate(self, data):
        data = super().validate(data)
        access_token_instance = AccessToken(data['access'])
        user_id = access_token_instance['user_id']
        user = get_object_or_404(User, id=user_id)
        update_last_login(None, user=user)
        return data


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()


class ChangePasswordSerializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class PersonalDataSerializer(serializers.Serializer):
    first_name = serializers.CharField(write_only=True, required=True)
    last_name = serializers.CharField(write_only=True, required=True)
    username = serializers.CharField(write_only=True, required=True)
    photo = models.ImageField(validators=[
        FileExtensionValidator(
            allowed_extensions=["jpg", "jpeg", "png", "svg", "heic", "heif", "webp"]
        )
    ])

    def cheak_username(self, username):
        if not self.cheak_username(username):  # Nimadir netoda shu joyida
            data = {
                "status": False,
                "messsage": "Username yaroqsiz"
            }

        if User.objects.filter(username=username).exists():
            data = {
                "status": False,
                "messsage": "Bu Username mavjud!"
            }
            raise ValidationError(data)
        return username

    def update(self, instance, validated_data):

        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.first_name)
        instance.username = validated_data.get('username', instance.first_name)
        instance.save()

        return instance


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields=("email", )


class PasswordResetConfirmSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField()