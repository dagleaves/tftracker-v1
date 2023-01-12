from django.urls import path

from .views import RegisterView, RetrieveUserView, GetCSRFTokenView, LoginView, LogoutView, CheckAuthenticatedView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('me/', RetrieveUserView.as_view(), name='current-user'),
    path('get-csrf/', GetCSRFTokenView.as_view(), name='get-csrf-token'),
    path('check-auth/', CheckAuthenticatedView.as_view(), name='check-auth')
]