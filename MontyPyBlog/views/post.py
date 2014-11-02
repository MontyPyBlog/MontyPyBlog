from django.http import HttpResponse
from MontyPyBlog.models import Post, User
from django.http import Http404

from rest_framework.decorators import api_view, parser_classes
from rest_framework.response import Response
from MontyPyBlog.serializers import PostSerializer, UserSerializer
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from django.views.decorators.csrf import csrf_exempt

"""
@TODO:
- Uploading files
- Sending uploaded files to an S3 bucket
- Getting the uploaded file slug(s)
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
        try:
            post_id = request.DATA.get('post_id')
            post = Post.objects.get(pk=post_id)

            serializer = PostSerializer(post)
        except Post.DoesNotExist:
            return Http404

        return Response(serializer.data)


@api_view(['POST'])
def post_post(request):
    if request.method == 'POST':
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
        try:
            post_id = request.DATA.get('post_id')
            post = Post.objects.get(pk=post_id)

        except Post.DoesNotExist:
            return Http404

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


@api_view(['POST'])
@parser_classes((MultiPartParser, FormParser))
def post_files(request):
    if request.method == 'POST':
        if request.DATA.get('file_upload_type') == 'featured_image':
            pass

        elif request.DATA.get('file_upload_type') == 'gallery_images':
            pass

        else:
            pass

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
