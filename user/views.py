from django.contrib.auth.hashers import make_password
from rest_framework import viewsets, status, authentication
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from user import serializers
from user.models import User
from user.services import UsersServices


class RegistrationModelViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.RegistrationSerializer

    def get_permissions(self):
        if self.action == 'change_login':
            return [IsAuthenticated(), ]
        return [AllowAny(), ]

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action == 'register':
            return serializers.RegistrationSerializer
        elif hasattr(self, 'action') and self.action == 'login':
            return serializers.AuthenticationSerializer
        elif self.action == 'change_login':
            return serializers.ChangeLoginSerializer

        return serializers.UserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            hashed_password = make_password(serializer.validated_data.get('password'))
            serializer.save(password=hashed_password)

            return Response(
                {'detail': 'User registered successfully'},
                status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = UsersServices.check_user(email, password)
            token, created = Token.objects.get_or_create(user=user)
            return Response(
                {
                    'username': user.username,
                    'token': str(token)
                },
                status=status.HTTP_200_OK
            )
        except:
            res = {'error': 'Check you credentials'}
            return Response(res, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def change_login(self, request):
        serializer = serializers.ChangeLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        new_login = serializer.validated_data.get('new_login')
        User.objects.filter(
            email=email).update(login=new_login)
        return Response(
            f"{new_login} is your login now",
            status=status.HTTP_201_CREATED
        )
