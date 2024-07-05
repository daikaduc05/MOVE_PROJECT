from django.db import models
from user.models import Users,Users_baned
# Create your models here.
class Category(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)
    thumbnail = models.URLField()
    is_show = models.BooleanField()
    image_url = models.URLField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    class Meta:
        managed = False
        db_table = 'categories'
class Video(models.Model):
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    thumbnail = models.URLField()
    url = models.URLField()
    user = models.ForeignKey(Users, on_delete=models.CASCADE, db_column='user_id')
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    keyword = models.CharField(max_length=255)
    is_comment = models.BooleanField()
    is_exist = models.BooleanField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()
    count_view = models.IntegerField()
    level = models.CharField(max_length=255,null= True)
    duration = models.CharField(max_length=255,null= True)
    title = models.CharField(max_length=255,null= True)
    duration_time = models.DurationField()
    is_hide = models.BooleanField()
    class Meta:
        managed = False
        db_table = 'videos'
