from rest_framework import serializers
from MontyPyBlog.models import Post, User

class PostSerializer(serializers.ModelSerializer):
    pk = serializers.Field()
    
    class Meta:
        model = Post
        fields = (
            'pk', 'author', 'title',
            'content', 'post_type', 'featured_image',
            'gallery_images', 'created_on')

class UserSerializer(serializers.ModelSerializer):
    pk = serializers.Field()

    class Meta:
        model = User
        fields = (
            '_id', 'username', 'email',
            'is_staff', 'created_on', 'last_login',
            'gallery_images', 'created_on')