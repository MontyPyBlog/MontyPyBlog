from django.http import HttpResponse
from MontyPyBlog.models import Post, User
import time
import django.middleware.csrf

from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from rest_framework.response import Response
from MontyPyBlog.serializers import PostSerializer, UserSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
import os
from boto.s3.connection import S3Connection
from boto.s3.key import Key
import threading
import imghdr


"""
@TODO:
- Site info in db (base url, base media url, etc)
"""


def index(request):
    posts_list = Post.objects.order_by('-created_on')[:3]
    output = 'List of posts: <br />' + ','.join([p.pk for p in posts_list])

    return HttpResponse(output)


"""
Handling posts
"""
@api_view(['GET'])
def get_post(request):
    if request.method == 'GET':
        if request.auth is None:
            return Response('Not Authenticated', status=status.HTTP_403_FORBIDDEN)

        try:
            post_id = request.DATA.get('post_id')
            post = Post.objects.get(pk=post_id)

            serializer = PostSerializer(post)
        except Post.DoesNotExist:
            return Http404

        return Response(serializer.data)


# For dev
@api_view(['GET'])
def get_csrf(request):
    if request.method == 'GET':
        return Response(django.middleware.csrf.get_token(request))
    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def post_post(request):
    if request.method == 'POST':
        if request.auth is None:
            return Response('Not Authenticated', status=status.HTTP_403_FORBIDDEN)

        user = User.objects.get(pk=request.DATA.get('author'))
        data = {
            'title': request.DATA.get('title'),
            'author': user.pk,
            'content': request.DATA.get('content'),
            'post_type': request.DATA.get('post_type'),
            'featured_image': request.DATA.get('featured_image'),
            'gallery_images': request.DATA.get('gallery_files'),
        }

        serializer = PostSerializer(data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PATCH'])
def patch_post(request):
    if request.method == 'PATCH':
        if request.auth is None:
            return Response('Not Authenticated', status=status.HTTP_403_FORBIDDEN)

        try:
            post_id = request.DATA.get('post_id')
            post = Post.objects.get(pk=post_id)

        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_id = request.DATA.get('author')
        user = User.objects.get(pk=user_id)

        data = {
            'title': request.DATA.get('title'),
            'author': user.pk,
            'content': request.DATA.get('content'),
            'post_type': request.DATA.get('post_type'),
            'featured_image': request.DATA.get('featured_image'),
            'gallery_images': request.DATA.get('gallery_images')
        }

        serializer = PostSerializer(post, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# TODO Add unique file names
# Can probably be rewritten more DRY-ly
@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser))
def post_files(request):
    if request.method == 'POST':
        if request.auth is None:
            return Response('Not Authenticated', status=status.HTTP_403_FORBIDDEN)

        post = Post.objects.get(pk=request.DATA.get('post_id'))

        # To prepend folder name
        s3_folder_name = 'MontyPyBlog/'

        if (request.DATA.get('file_upload_type') == 'gallery_images') or (len(request.FILES) > 1):
            file_upload_type = 'gallery_images'
        elif request.DATA.get('file_upload_type') == 'featured_image':
            file_upload_type = 'featured_image'

        accepted_file_types = ['jpeg', 'gif', 'png']

        def upload(file, key_name):
            if imghdr.what(file) not in accepted_file_types:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Boto connections aren't thread safe
            # Secret and key are set in environment variables
            s3 = S3Connection()
            bucket_name = os.environ['S3_BUCKET_NAME']
            bucket = s3.get_bucket(bucket_name)
            key_object = Key(bucket)

            key_object.key = s3_folder_name + key_name
            key_object.set_contents_from_file(file)
            key_object.make_public()

            image_url = key_object.generate_url(expires_in=0, query_auth=False)

            return image_url

        # Bottleneck will be connecting to S3, so we thread
        # Research how to get return values for threads
        file_urls = []
        for filename, file in request.FILES.iteritems():
            key_name = str(time.time()) + '-' + file.name
            t = threading.Thread(target=upload, args=(file, key_name)).start()
            file_urls.append(os.environ['S3_BUCKET_LOCATION'] + key_name)

        data = {
            file_upload_type: ','.join(file_urls),
            'post_id': post.pk,
        }

        serializer = PostSerializer(post, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # Else keep going and return 405

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)