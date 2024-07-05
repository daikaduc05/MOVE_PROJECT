from rest_framework import serializers
import re
from .models import Users
from django.shortcuts import get_object_or_404
from Common.messenge import NOT_MATCH_PASSWORD,WRONG_FORM_EMAIL,WRONG_FORM_PASSWORD,OLD_AND_NEW
from Common.Regex import remail,rpassword
class VideoSerializer(serializers.Serializer):
    file_name = serializers.CharField()
    thumbnail = serializers.FileField(required = False)
    user = serializers.CharField(required = False)
    category = serializers.CharField(required = False)
    keyword = serializers.CharField(required = False)
    title = serializers.CharField()
    description = serializers.CharField()

