from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializer import VideoSerializer
import requests
from .service import upload_video_and_get_the_url
class UploadVideo(APIView):
    def post(self, request, *args, **kwargs):
        try:
            serialize = VideoSerializer(data=request.data)
            if serialize.is_valid():
                data = serialize.validated_data
                video_url = upload_video_and_get_the_url(file_name=data['file_name'],name=data['title'],description=data['description'])
                if video_url:
                    return Response({"message": "Upload successful", "video_url": video_url}, status=status.HTTP_200_OK)
                else:
                    return Response({"message": "Upload failed"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(serialize.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Exception: {e}")
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
