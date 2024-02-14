from django.conf import settings
from drf_spectacular.utils import extend_schema
from rest_framework.generics import RetrieveAPIView, RetrieveUpdateDestroyAPIView, get_object_or_404

from .models import ConfirmationCode
from rest_framework.permissions import AllowAny
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework.permissions import IsAuthenticated
from .forms import CaptchaSerializer
from rest_framework import generics, status


class UserRegistrationView(APIView):
    permission_classes = [AllowAny]
    serializer_class = UserRegistrationSerializer
    @extend_schema(tags=['Registration and Authentication'])


    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            confirmation_code = user.confirmation_code
            subject = 'Confirmation code'
            message = f'Your confirmation code is: {confirmation_code}'
            from_email = 'bapaevmyrza038@gmail.com'  
            recipient_list = [user.email]

            send_mail(subject, message, from_email, recipient_list, fail_silently=False)

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request):
        confirmation_code = request.data.get('confirmation_code')
        if not confirmation_code:
            return Response({'error': 'Confirmation code is required.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = CustomUsers.objects.get(confirmation_code=confirmation_code, is_active=False)
        except CustomUsers.DoesNotExist:
            return Response({'error': 'Invalid or expired confirmation code.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.is_active = True
        user.save()

        return Response({'message': 'Email confirmed successfully.'}, status=status.HTTP_200_OK)
    

class CustomUserLoginView(TokenObtainPairView):
    @extend_schema(tags=['Registration and Authentication'])

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        tokens = response.data

        # Получаем access токен из ответа
        access_token = tokens.get('access', None)

        if access_token:
            # Парсим access токен
            access_token_instance = AccessToken(access_token)
            # Получаем полезную нагрузку (payload)
            payload = access_token_instance.payload
            # Получаем id пользователя из полезной нагрузки
            user_id = payload['user_id']
            # Добавляем id пользователя в ответ
            tokens['user_id'] = user_id

        return Response(tokens, status=status.HTTP_200_OK)


class CustomUserTokenRefreshView(APIView):
    @extend_schema(tags=['Registration and Authentication'])

    
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)
            return Response({'access': access_token,
                             'refresh':token}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)
        

class ChangePasswordView(APIView):

    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

    @extend_schema(tags=['Registration and Authentication'])
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            old_password = serializer.data.get("old_password")
            new_password = serializer.data.get("new_password")

            if not user.check_password(old_password):
                return Response({"detail": "Old password is incorrect."}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save()

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

class ChangeUsernameView(APIView):

    permission_classes = [IsAuthenticated]

    @extend_schema(tags=['Registration and Authentication'])
    def post(self, request):
        serializer = ChangeUsernameSerializer(data=request.data)
        if serializer.is_valid():
            user = request.user
            new_username = serializer.data.get("new_username")

            user.username = new_username
            user.save()

            return Response({"detail": "Username changed successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(generics.CreateAPIView):

    serializer_class = ForgotPasswordSerializer
    queryset = CustomUsers.objects.all()
    permission_classes = [AllowAny]

    @extend_schema(tags=['Registration and Authentication'])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        users = CustomUsers.objects.filter(email=email)

        if not users.exists():
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        confirmation_code = get_random_string(length=20)

        user = users[0]  
        ConfirmationCode.objects.create(user=user, code=confirmation_code)

        subject = 'Confirmation Code'
        message = f'Your confirmation code is: {confirmation_code}'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list, fail_silently=False)

        return Response({'message': 'Confirmation code sent successfully.'})


class ResetPasswordView(generics.CreateAPIView):

    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=['Registration and Authentication'])
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data.get("email")
            confirmation_code = serializer.validated_data.get("confirmation_code")
            new_password = serializer.validated_data.get("new_password")
            
            try:
                confirmation = ConfirmationCode.objects.get(user__email=email, code=confirmation_code)
            except ConfirmationCode.DoesNotExist:
                return Response({"detail": "Invalid or expired confirmation code or wrong email."}, status=status.HTTP_400_BAD_REQUEST)

            user = confirmation.user
            user.set_password(new_password)
            user.save()

            confirmation.delete()

            return Response({"detail": "Password changed successfully."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CaptchaView(APIView):

    permission_classes = [AllowAny]

    @extend_schema(tags=['Registration and Authentication'])
    def post(self, request, *args, **kwargs):
        serializer = CaptchaSerializer(data=request.data)
        if serializer.is_valid():
            return Response({'message': 'Captcha is valid'})
        else:
            return Response(serializer.errors, status=400)


class UserListView(generics.ListAPIView):

    permission_classes = [IsAuthenticated]

    serializer_class = UserSerializer

    queryset = CustomUsers.objects.all()


class UserSearchView(APIView):
    permission_classes = [IsAuthenticated]
    @extend_schema(tags=['Registration and Authentication'])

    def get(self, request, pk):
        # Получаем пользователя по идентификатору (primary key)
        user = get_object_or_404(CustomUsers, pk=pk)

        # Сериализуем пользователя
        serializer = UserSerializer(user)

        return Response(serializer.data)


class UserUpdateView(RetrieveUpdateDestroyAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @extend_schema(tags=['Registration and Authentication'])

    def get_object(self):
        return self.request.user