from django.shortcuts import render,get_object_or_404
from .service import UserService
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import RegisterSerializer,ActiveSerializer,UpdateSerializer,SendEmailSerializer,LoginSerializer,NewPasswordSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import status
from .service import UserService
from django.core.mail import send_mail
from django.db import IntegrityError
from Common.messenge import INTERGRITY_EMAIL,NOT_EXIST_EMAIL,IS_NOT_ACTIVED,TMP_BANED,FOREVER_BANED,WRONG_INFORMATION
from .models import Users,Users_baned
from .token import RedisTokenBackend
from datetime import datetime
# Create your views here.
class Register(APIView):
    def post(self,request,format = None):
        try:
            
            serialize = RegisterSerializer(data = request.data)
            
            if serialize.is_valid():
                UserService.create(
                    request.data['password'],
                    request.data['email'],
                )
                UserService.create_user_banned(request.data['email'])
                UserService.send_otp(request.data["email"])
                return Response("Created",status= status.HTTP_201_CREATED)
            else:
                return Response(serialize.errors,status= status.HTTP_400_BAD_REQUEST)
            
        except IntegrityError :
            return Response(INTERGRITY_EMAIL,status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response("?",status=status.HTTP_400_BAD_REQUEST)      

class Active(APIView):
    def post(self,request,*args, **kwargs):
        try:
            serialize = ActiveSerializer(data= request.data)
            if serialize.is_valid() : 
                data = serialize.validated_data
                if UserService.check_email(**data) :
                    UserService.update(email= request.data["email"],is_actived=1)
                    
                    return Response("Actived!",status=status.HTTP_202_ACCEPTED)
                else:
                    return Response("Invalid",status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST) 
            
class SendEmail(APIView):
    def post(self,request,*args, **kwargs):
        try:
            serialize = SendEmailSerializer(data= request.data)
            if serialize.is_valid():
                data = serialize.validated_data
                UserService.send_otp(**data)
                return Response("Sent!",status=status.HTTP_200_OK)
        except Exception as e:
            return Response(NOT_EXIST_EMAIL,status=status.HTTP_404_NOT_FOUND) 

class Login(APIView):
    def post(self,request,*args, **kwargs):
        try:    
            
            serialize = LoginSerializer(data=request.data)
         
            if not serialize.is_valid():
                return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
            
            #print(request.data['email'])
            user = get_object_or_404(Users,email = request.data['email'])
           
            user = user.authenticate(password= request.data['password'])
            
            tokens = RedisTokenBackend()
            if user is not None :
                try:
                    is_ban = Users_baned.objects.get(user_id = user.id)
                    now = datetime.now()
                    if is_ban.ban_expired_at == None:
                        return Response(tokens.create_token(email=request.data['email']),status=status.HTTP_200_OK)
                    if is_ban.is_permaban == True:
                        return Response(FOREVER_BANED,status=status.HTTP_403_FORBIDDEN)
                    elif is_ban.ban_expired_at > now :
                        return Response(TMP_BANED,status=status.HTTP_403_FORBIDDEN)
                    else:
                        return Response(tokens.create_token(email=request.data['email']),status=status.HTTP_200_OK)
                except Users_baned.DoesNotExist:
                    if (user.is_actived == 1):
                        return Response(tokens.create_token(email=request.data['email']),status=status.HTTP_200_OK)
                    else:
                        return Response(IS_NOT_ACTIVED,status=status.HTTP_403_FORBIDDEN)
            else:
                return Response(WRONG_INFORMATION,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)
        except Exception as e:
            return Response("Unknow",status=status.HTTP_400_BAD_REQUEST)
class ChangePassword(APIView):
    def post(self,request,*args, **kwargs):
        try:
            serialize = NewPasswordSerializer(data=request.data)
            if not serialize.is_valid():
                return Response(serialize.errors,status=status.HTTP_400_BAD_REQUEST)
            
            user = get_object_or_404(Users,email = request.data['email'])

            user = user.authenticate(password= request.data['old_password'])
            
            if user is not None:    
                UserService.change_password(email=user.email,new_password=request.data['new_password'])
                return Response("Changed !",status=status.HTTP_202_ACCEPTED)
            else:
                return Response(WRONG_INFORMATION,status=status.HTTP_203_NON_AUTHORITATIVE_INFORMATION)    
        except Exception as e:
            return Response("Unknown",status=status.HTTP_400_BAD_REQUEST)
