from dj_rest_auth.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator

from django.contrib.auth import login, logout, authenticate

from rest_framework import status
from rest_framework.response import Response

from .serializers import UserRegistrationSerializer, UserSerializer


@method_decorator(ensure_csrf_cookie, name='dispatch')
class GetCSRFToken(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        return Response({'success': 'CSRF token set'})


class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'success': 'User authenticated'})
        else:
            return Response({'error': 'Invalid credentials'})


class LogoutView(APIView):
    def post(self, request, format=None):
        try:
            logout(request)
            return Response({"success": "Logged out successfully"})
        except:
            return Response({'error': 'Something went wrong while logging out'})


class RegisterView(APIView):
    def post(self, request):
        data = request.data
        serializer = UserRegistrationSerializer(data=data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.create(serializer.validated_data)
        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_201_CREATED)


class RetrieveUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user = UserSerializer(user)

        return Response(user.data, status=status.HTTP_200_OK)