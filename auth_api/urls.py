from django.urls import path
from auth_api.views import ChangePassword, ProfileView, ResetPassword, ResetPasswordEmail, SignUpView, LoginView


urlpatterns = [
    path('signup/', SignUpView.as_view(), name= 'signup'),
    path('login/', LoginView.as_view(), name= 'login'),
    path('profile/', ProfileView.as_view(), name= 'profile'),
    path('changepassword/', ChangePassword.as_view(), name= 'changepassword'),
    path('resetpasswordlink/', ResetPasswordEmail.as_view(), name= 'resetpasswordlink'),
    path('resetpassword/<uid>/<token>/', ResetPassword.as_view(), name= 'resetpassword'),        
]
