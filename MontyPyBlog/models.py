from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length = 255)
    content = models.TextField()
    POST = 'post'
    GALLERY = 'gallery'
    POST_TYPES = (
        (POST, 'Post'),
        (GALLERY, 'Gallery'),
    )
    post_type = models.CharField(max_length = 7, choices = POST_TYPES)
    post = models.ForeignKey(User)
    featured_image = models.SlugField('S3 Bucket slug', max_length = 255)
    gallery_images = models.SlugField('S3 Bucket Slug', max_length = 255)
    created_on = models.DateTimeField(auto_now = True)

class User(models.Model):
    username = models.CharField(max_length = 50)
    password = models.CharField(max_length = 255)
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now = True)
    # Django fields for users:
    groups = models.ManyToManyField('Group')
    user_permissions = models.ManyToManyField('Permission')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    last_login = models.DateTimeField()

class Permission(models.Model):
    name = models.CharField('Ex: Can Vote', max_length = 50)
    content_type = models.ForeignKey(ContentType, related_name = 'content_type')
    codename = models.CharField('Ex: can_vote', max_length = 100)

class Group(models.Model):
    name = models.CharField(max_length = 80)
    permissions = models.ManyToManyField('Permission')

class Security(models.Model):
    # Oauth implementation
    pass