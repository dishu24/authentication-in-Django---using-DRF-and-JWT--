from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import ChangePasswordSerializer, LoginSerializer, ProfileSerializer, ResetPasswordEmailSerializer, ResetPasswordSerializer, SignUpSerializer , ProfileSerializer, ChangePasswordSerializer
from django.contrib.auth import authenticate
from .renders import UserRenders
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated


# gentrate token 
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

class SignUpView(APIView):
    renderer_classes =[UserRenders]
    def post(self, request, format=None):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response({'token':token,'msg':'account created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
class LoginView(APIView):
    renderer_classes =[UserRenders]
    def post(self, request, format= None):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({'token':token,"msg":'login succesfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'errors':{'non_fields_errors':'Email or password is not valid'}}, status = status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProfileView(APIView):
    renderer_classes =[UserRenders]
    permission_classes= [IsAuthenticated]
    def get(self, request, format=None):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data, status = status.HTTP_200_OK)
    
class ChangePassword(APIView):
    renderer_classes =[UserRenders]
    permission_classes= [IsAuthenticated]
    def post(self, request, format=None):
        serializer = ChangePasswordSerializer(data=request.data, context={'user':request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password change successfully'} ,status = status.HTTP_200_OK)
        
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class ResetPasswordEmail(APIView):
    renderer_classes =[UserRenders]
    def post(self, request, format=None):
        serializer = ResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'Link Send , please check your email'} ,status = status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

class ResetPassword(APIView):
    renderer_classes =[UserRenders]
    def post(self, request,uid, token, format=None):
        serializer = ResetPasswordSerializer(data=request.data, context={'uid':uid,'token':token})
        if serializer.is_valid(raise_exception=True):
            return Response({'msg':'password reset successfully'} ,status = status.HTTP_200_OK)
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)