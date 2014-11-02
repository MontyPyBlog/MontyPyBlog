from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from bson.objectid import ObjectId

from bson.json_util import dumps
import bson


"""
@TODO Create/research a proper json serializer for the api
"""

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    POST = 'post'
    GALLERY = 'gallery'
    POST_TYPES = (
        (POST, 'Post'),
        (GALLERY, 'Gallery'),
    )
    post_type = models.CharField(max_length=7, choices=POST_TYPES)
    author = models.CharField(max_length=80, blank=True, null=True)
    featured_image = models.SlugField(
        'S3 Bucket slug for featured image',
        max_length=255)
    gallery_images = models.SlugField(
        'S3 Bucket slugs for gallery images',
        max_length=255,
        blank=True)
    created_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        output = {
            'Id' : self.pk,
            'Title' : self.title,
            'AuthorId' : self.author_id,
            'Content' : self.content,
            'Post Type' : self.post_type,
            'Featured Image' : self.featured_image,
            'Gallery Images' : self.gallery_images,
            'Created On' : str(self.created_on),
        }
        # return '<pre>' + dumps(output, sort_keys=True, indent=4, separators=(',', ': '), default=bson.json_util.object_hook) + '</pre>'
        return self.pk       


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now=True)
    # Django fields for users:
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    last_login = models.DateTimeField(blank=True, null=True)

    def __unicode__(self):
        output = {
            'Id' : self.pk,
            'Username' : self.username,
            'Email' : self.email,
            'Created On' : str(self.created_on),
            'Last Login' : str(self.last_login),
            'Admin' : self.is_staff,
        }
        return self.pk


class Security(models.Model):
    # Oauth implementation
    pass
