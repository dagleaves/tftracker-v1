from django.urls import path

from .views import RegisterView, RetrieveUserView, GetCSRFToken, LoginView, LogoutView, CheckAuthenticatedView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', RetrieveUserView.as_view(), name='current-user'),
    path('get-csrf/', GetCSRFToken.as_view(), name='get-csrf-token'),
    path('check-auth/', CheckAuthenticatedView.as_view(), name='check-auth')
]