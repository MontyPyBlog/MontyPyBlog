from django.http import HttpResponse
from MontyPyBlog.models import Post, User
from django.http import Http404
from bson.objectid import ObjectId

from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from MontyPyBlog.serializers import PostSerializer
from rest_framework import status

from bson.json_util import dumps
import bson

from django.views.decorators.csrf import csrf_exempt

def index(request):
    posts_list = Post.objects.order_by('-created_on')[:3]
    output = 'List of posts: <br />' + ','.join([p.pk for p in posts_list])
    return HttpResponse(output)


"""
Handling posts
"""
@api_view(['GET'])
def get_post(request, post_id):
    if request.method == 'GET':
        try:
            post = Post.objects.get(pk=post_id)

            serializer = PostSerializer(post)
        except Post.DoesNotExist:
            return HttpResponse(status=404)
        return Response(serializer.data)


def patch_post(request, post_id):
    return HttpResponse("You're looking to edit post with id %s" % post_id)

@api_view(['POST'])
def post_post(request, user_id):
    if request.method == 'POST':
        if (request.DATA.get('post_type').lower() == 'post'):
            gallery_files = request.DATA.get('gallery_images')

        user = User.objects.get(pk=user_id)
        data = {
            'title' : request.DATA.get('title'),
            'author' : user.pk,
            'content' : request.DATA.get('content'),
            'post_type' : request.DATA.get('post_type'),
            'featured_image' : request.DATA.get('featured_image'),
            'gallery_images' : gallery_files,
        }

        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_created)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return 'Method not allowed'


"""
Handling Users
"""
def post_user(request):
    return HttpResponse("You're posting a user!")


def get_user(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except Post.DoesNotExist:
        raise Http404
    return HttpResponse(user)


def patch_user(request, user_id):
    return HttpResponse("You're requesting to edit a user with id %s" % user_id)


def post_login(request, user_id):
    return HttpResponse("You're logging in as id %s" % user_id)


def post_logout(request, user_id):
    return HttpResponse("You're logging out of id %s" % user_id)


"""
URL Structure from PHP CMS:
Route::get('/', array('as' => 'home', 'uses' => 'ArticleController@getArticles'));
//Route::get('article/post', 'ArticleController@postArticles');
Route::get('article/{id}', 'ArticleController@getArticle');
Route::get('user/{id}/testing', 'ArticleController@getThing');
Route::get('login', 'UserController@getLogin')->before('guest');
Route::get('logout', 'UserController@getLogout')->before('auth');
Route::get('profile/{id}', 'UserController@getProfile');

Route::post('article/post', 'ArticleController@postArticles')->before('auth');
Route::post('article/comment', 'ArticleController@postComment')->before('auth');
Route::post('login', 'UserController@postLogin');

Route::get('dbmigrate', 'DbmigrateController@index');


// Put into group with before filter
Route::get('admin', array('as' => 'admin' , 'uses' => 'AdminController@getAdmin'));
Route::get('admin/submit', array('as' => 'article.submit', function()
    {
        return View::make('admin-submit');
    }));
Route::get('admin/edit/{id}', array('as' => 'article.update', function($id) 
    {
        // return our view and Post information
        return View::make('admin-edit')
            ->with('post', Post::find($id));
    }));

Route::post('admin/submit/article', array('as' => 'article.post', 'uses' => 'AdminController@postArticle'));
Route::post('admin/edit/{id}', array('as' => 'article.patch', 'uses' => 'AdminController@patchArticle'));
"""
