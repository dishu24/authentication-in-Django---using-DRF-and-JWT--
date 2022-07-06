from django.forms import ValidationError

from rest_framework import serializers
from auth_api import utils
from .utils import Util
from .models import User
from django.utils.encoding import smart_str, force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class SignUpSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = User
        fields = ['email','name','password','password2']
        extra_kwargs = {
            'password':{'write_only':True}
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError("password doesn't match.")
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    class Meta:
        model = User
        fields = ['email','password']

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','email','name']

class ChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only= True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only= True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')
        if password != password2:
            raise serializers.ValidationError("password doesn't match.")
        user.set_password(password)
        user.save()
        return attrs

class ResetPasswordEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email= attrs.get('email')
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(force_bytes(user.id))
            print('encode uid-- ',uid)
            token = PasswordResetTokenGenerator().make_token(user)
            print('token--- ', token)
            link = 'http://localhost:3000/resetpasswordlink/'+uid+'/'+token
            print('password reset link --- ', link)
            
            # email send 
            body= 'Click below link to reset your password'+link
            data= {
                "subject":'Reset Your Password',
                "body": body,
                "to_email": user.email
            }
            Util.send_email(data)
            return attrs
        else:
            raise ValidationError('You are not registered User.')

class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(style={'input_type':'password'}, write_only= True)
    password2 = serializers.CharField(style={'input_type':'password'}, write_only= True)
    class Meta:
        fields = ['password','password2']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            password2 = attrs.get('password2')
            uid = self.context.get('uid')
            token = self.context.get('token')
            if password != password2:
                raise serializers.ValidationError("password doesn't match.")
            id = smart_str(urlsafe_base64_decode(uid))
            user = User.objects.get(id=id)
            if not PasswordResetTokenGenerator().check_token(user,token):
                raise ValidationError('Token is not valid or Expired')
            user.set_password(password)
            user.save()
            return attrs
        except DjangoUnicodeDecodeError as identifier:
            PasswordResetTokenGenerator().check_token(user,token)
            raise ValidationError('Token is not valid or Expired')