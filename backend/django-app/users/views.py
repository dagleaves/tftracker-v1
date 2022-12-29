import re
from dj_rest_auth.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
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


@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        password = data['password']

        user = authenticate(email=email, password=password)

        if user is not None:
            login(request, user)
            return Response({'success': 'User authenticated'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        try:
            logout(request)
            return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)
        except:
            return Response({'error': 'Something went wrong while logging out'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@method_decorator(ensure_csrf_cookie, name='dispatch')
class CheckAuthenticatedView(APIView):
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'isAuthenticated': 'true'}, status=status.HTTP_200_OK)
        return Response({'isAuthenticated': 'false'}, status=status.HTTP_401_UNAUTHORIZED)



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