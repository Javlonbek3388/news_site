from django.contrib.auth import authenticate, login
from rest_framework import serializers
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from rest_framework.generics import CreateAPIView, UpdateAPIView, GenericAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.conf import settings
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str
from .models import User
from .serializers import (
    RegisterSerializer,
    LoginSerializer,
    UpdateAccessSerializer,
    LogoutSerializer,
    ChangePasswordSerializer,
    PersonalDataSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer, )
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class RegisterApiView(CreateAPIView):
    permission_classes = [AllowAny, ]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class UpdateAccessApiView(TokenRefreshView):
    serializer_class = UpdateAccessSerializer




@api_view(['POST'])
@permission_classes([AllowAny])
def user_login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutApiView(APIView):
    serializer_class = LogoutSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data
        )
        serializer.is_valid(
            raise_exception=True
        )

        try:
            refresh_token = self.request.dat['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()

            data = {"status": True, "message": "Siz tizimdan muvafaqqiyatli chiqdingiz! "}

            return Response(data=data, status=205)
        except Exception as e:
            data = {"status": False, "message": str(e)}
            return Response(data=data, status=405)


class ChangePasswordView(UpdateAPIView):
    """
    An endpoint for changing password.
    """
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Password muvofaqqiyatli o\'zgartirildi',

            }

            return Response(response)

        return Response


class PersonalDataApiView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = PersonalDataSerializer
    http_method_names = ['put', 'patch']

    def get_queryset(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        data = {
            'status': True,
            'message': "Siz ro'yxatdan o'tdingiz!",
            'auth_status': self.request.user.auth_status
        }
        return Response(data)

    def partial_update(self, request, *args, **kwargs):
        super(PersonalDataApiView).partial_update(request, *args, *kwargs)
        data = {
            'status': True,
            'message': "Siz ro'yxatdan o'tdingiz",
            'auth_status': self.request.user.auth_status
        }
        return Response(data)


class PasswordResetApiView(APIView):
    serializer_class = PasswordResetSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.filter(email=email).first()

            if user:
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                reset_link = f"http://127.0.0.1:8000/reset-password/{uid}/{token}/"
                send_mail(
                    'Password Reset',
                    f'Use the following link to reset your password: {reset_link}',
                    'javlonbekinomjonovich@gmail.com',
                    [email],
                    fail_silently=False,
                )

            return Response({'message': 'Password reset link sent to your email.'}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            uid = serializer.validated_data['uid']
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            try:
                user_id=force_str(urlsafe_base64_decode(uid))
                user=User.objects.get(pk=user_id)
            except (TypeError, ValueError, OverflowError,  User.DoesNotExist):
                user=None
            if user is not None and default_token_generator.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password muvafaqqiyatli o\'zgartirildi'}, status=status.HTTP_200_OK)

            return Response({'message': 'Link xato!'}, status=status.HTTP_400_BAD_REQUEST)
