import os
import vimeo
from dotenv import load_dotenv
from .models import Video
from django.utils import timezone
from datetime import timedelta
load_dotenv()

def create_client():
    access_token = os.getenv('VIMEO_ACCESS_TOKEN')
    client_id = os.getenv('VIMEO_ID')
    client_secret = os.getenv('VIMEO_SECRET_CLIENTS')

    client = vimeo.VimeoClient(
        token=access_token,
        key=client_id,
        secret=client_secret
    )
    return client

def upload_video_and_get_the_url(file_name, name, description, id, category):
    try:
       
        client = create_client()
        
    
        url = client.upload(file_name, data={
            'name': name,
            'description': description
        })
        
    

        video_id = url.split('/')[-1]
        
        curent_time = timezone.now()
        video_url = f"https://player.vimeo.com/video/{video_id}"
        video = Video(
             description = description,
             thumbnail = None,
             url = video_url,
             user_id = id,
             category_id = category,
             keyword = None,
             is_exist = False,
             is_comment = False,
             created_at = curent_time,
             updated_at = curent_time,
             count_view = 0,
             level = None,
             duration = None,
             title = name,
             duration_time = timedelta(seconds=14),
             is_hide = False
         )
        video.save()
        return video_url
      #  print(f"Video URL: {video_url}")
    
    except vimeo.exceptions.VideoUploadFailure as e:
        print(f"Failed to upload video: {str(e)}")
    
    except vimeo.exceptions.UploadAttemptCreationFailure as e:
        print(f"Failed to create upload attempt: {str(e)}")
        print(f"Error details: {e}")
    
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")


# file_name = r'C:\Users\Admin\Videos\1 Second Video (1).mp4'
# name = 'concac'
# description = 'dit me may'


# upload_video(file_name=file_name, name=name, description=description)
