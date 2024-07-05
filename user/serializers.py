from rest_framework import serializers
import re
from .models import Users
from django.shortcuts import get_object_or_404
from Common.messenge import NOT_MATCH_PASSWORD,WRONG_FORM_EMAIL,WRONG_FORM_PASSWORD,OLD_AND_NEW
from Common.Regex import remail,rpassword
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fiedls = '__all__'

class RegisterSerializer(serializers.Serializer):
    username = serializers.CharField(required = False)
    email = serializers.EmailField()
    password = serializers.CharField(min_length=8)
    repeat_password = serializers.CharField(min_length=8)    
    def validate(self, data):
        if data['password'] != data['repeat_password']:
            raise serializers.ValidationError(NOT_MATCH_PASSWORD)
        elif not re.match(remail,data['email']) :
            raise serializers.ValidationError(WRONG_FORM_EMAIL)
        elif not re.match(rpassword,data['password']):
            raise serializers.ValidationError(WRONG_FORM_PASSWORD)
        return data
class ActiveSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()
    def validate(self, data):
        if not re.match(remail,data['email']) :
            raise serializers.ValidationError(WRONG_FORM_EMAIL)
        return data

class UpdateSerializer(serializers.Serializer):
    email = serializers.EmailField()
    username = serializers.CharField(required = False)
    fullname = serializers.CharField(required = False)
    birthday = serializers.DateField(required = False) 
    country = serializers.CharField(required = False)
    city = serializers.CharField(required = False)
    state = serializers.CharField(required = False)
    avatar_url = serializers.CharField(required = False)
    is_actived = serializers.CharField(required = False)
    is_verified = serializers.CharField(required = False)
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    def validate(self, data):
        if not re.match(remail,data['email']) :
            raise serializers.ValidationError(WRONG_FORM_EMAIL)
        elif not re.match(rpassword,data['password']):
            raise serializers.ValidationError(WRONG_FORM_PASSWORD)
        else :
            return data
class SendEmailSerializer(serializers.Serializer):
    email = serializers.EmailField()
    def validate(self, data):
        user = get_object_or_404(Users, email = data['email'])
        return data
class NewPasswordSerializer(serializers.Serializer):
    email = serializers.CharField()
    old_password = serializers.CharField()
    new_password = serializers.CharField()
    repeat_password = serializers.CharField()
    def validate(self, data):
        if data['repeat_password'] == data['old_password']:
            raise serializers.ValidationError(OLD_AND_NEW)
        elif data['new_password'] != data['repeat_password']:
            raise serializers.ValidationError("NOT_MATCH_PASSWORD")
        elif not (re.match(rpassword,data['new_password'])):
            raise serializers.ValidationError(WRONG_FORM_PASSWORD)
        elif not re.match(rpassword,data['old_password']):
            raise serializers.ValidationError(WRONG_FORM_PASSWORD)
        elif not (re.match(remail,data['email'])):
            raise serializers.ValidationError(WRONG_FORM_EMAIL)
        elif not (re.match(rpassword,data['repeat_password'])):
            raise serializers.ValidationError(WRONG_FORM_PASSWORD)
        else:
            return data 