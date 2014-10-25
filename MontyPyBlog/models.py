from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType


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
    author = models.ForeignKey(User, blank=True, null=True)
    featured_image = models.SlugField(
        'S3 Bucket slug for featured image',
        max_length=255)
    gallery_images = models.SlugField(
        'S3 Bucket slugs for gallery images',
        max_length=255)
    created_on = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        output = [
            self.title, self.content, self.post_type,
            self.featured_image, self.gallery_images, self.created_on]
        return self.title


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=255)
    email = models.EmailField()
    created_on = models.DateTimeField(auto_now=True)
    # Django fields for users:
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    last_login = models.DateTimeField()

    def __unicode__(self):
        output = [
            self.username, self.email, self.created_on,
            self.last_login]
        return self.username


class Security(models.Model):
    # Oauth implementation
    pass
