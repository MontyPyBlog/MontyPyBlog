from django.http import HttpResponse
from MontyPyBlog.models import Post, User
from django.http import Http404

from rest_framework.decorators import api_view
from rest_framework.response import Response
from MontyPyBlog.serializers import PostSerializer, UserSerializer
from rest_framework import status

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
def get_post(request, post_id):
    if request.method == 'GET':
        try:
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

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PATCH'])
def patch_post(request):
    if request.method == 'PATCH':
        try:
            postId = request.DATA.get('postId')
            post = Post.objects.get(pk=postId)

        except Post.DoesNotExist:
            return Http404

        userId = request.DATA.get('author')
        user = User.objects.get(pk=userId)

        data = {
            'title' : request.DATA.get('title'),
            'author' : user.pk,
            'content' : request.DATA.get('content'),
            'post_type' : request.DATA.get('post_type'),
            'featured_image' : request.DATA.get('featured_image'),
            'gallery_images' : request.DATA.get('gallery_images')
        }

        serializer = PostSerializer(post, data=data)

        if serializer.is_valid():
            serializer.save()

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


"""
Handling Users
"""
@api_view(['POST'])
def post_user(request):
    if request.method == 'POST':
        data = {
            'username' : request.DATA.get('username'),
            'email' : request.DATA.get('email'),
            'password' : request.DATA.get('password'),
        }

        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['GET'])
def get_user(request, user_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=user_id)

            data= {
                'pk' : user.pk,
                'username' : user.username
            }
        except User.DoesNotExist:
            raise Http404

        serializer = UserSerializer(data=data)

        return Response(user.email)

    else:
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['PATCH'])
def patch_user(request):
    if request.method == 'PATCH':
        try:
            userId = request.DATA.get('userId')
            user = User.objects.get(pk=userId)
        except User.DoesNotExist:
            raise Http404

        data = {
            'username' : request.DATA.get('username'),
            'email' : request.DATA.get('email'),
            'password' : request.DATA.get('password'),
        }

        serializer = UserSerializer(user, data=data)

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
