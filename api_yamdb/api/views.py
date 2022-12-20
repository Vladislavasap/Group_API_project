from django.shortcuts import render
from django.core.mail import EmailMessage
from rest_framework import permissions, status
from .serializers import GetTokenSerializer, SignUpSerializer

class GetToken(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Пользователь отсутствует.'},
                status=status.HTTP_404_NOT_FOUND
            )

        if str(data.get('confirmation_code')) == str(user.confirmation_code):
            token = RefreshToken.for_user(user).access_token
            return Response(
                {'token': str(token)},
                status=status.HTTP_201_CREATED
            )
        a = str(data.get('confirmation_code'))
        b = str(user.confirmation_code)
        print(a)
        print(b)
        return Response(
            {'confirmation_code': 'Ошибка кода подтверждения'},
            status=status.HTTP_400_BAD_REQUEST
        )


class SignUp(APIView):
    permission_classes = (permissions.AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(body=data['email_body'], to=[data['to_email']])
        email.send()

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        data = {
            'email_body': f'{user.username}, {user.confirmation_code}',
            'to_email': user.email,
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)

