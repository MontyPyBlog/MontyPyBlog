from django.http import HttpResponse
from MontyPyBlog.models import User
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from MontyPyBlog.serializers import UserSerializer
from rest_framework import status

from django.views.decorators.csrf import csrf_exempt

"""
Handling Users
"""
@api_view(['POST'])
def post_user(request):
    if request.method == 'POST':
        if request.auth is None:
            return Response('Not Authenticated', status=status.HTTP_403_FORBIDDEN)

        data = {
            'username': request.DATA.get('username'),
            'email': request.DATA.get('email'),
            'password': request.DATA.get('password'),
        }

        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_user(request):
    if request.method == 'GET':
        if request.auth is None:
            return Response('Not Authenticated', status=status.HTTP_403_FORBIDDEN)

        try:
            user_id = request.DATA.get('user_id')
            user = User.objects.get(pk=user_id)

            data = {
                'pk': user.pk,
                'username': user.username
            }
        except User.DoesNotExist:
            raise Http404

        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH'])
def patch_user(request):
    if request.method == 'PATCH':
        if request.auth is None:
            return Response('Not Authenticated', status=status.HTTP_403_FORBIDDEN)

        try:
            user_id = request.DATA.get('user_id')
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            raise Http404

        data = {
            'username': request.DATA.get('username'),
            'email': request.DATA.get('email'),
            'password': request.DATA.get('password'),
        }

        serializer = UserSerializer(user, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


def post_login(request, user_id):
    return HttpResponse("You're logging in as id %s" % user_id)


def post_logout(request, user_id):
    return HttpResponse("You're logging out of id %s" % user_id)
