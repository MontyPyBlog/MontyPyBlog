from django.http import HttpResponse


def index(request):
    return HttpResponse('Hello, word. You\'re at the blog homepage')

"""
Handling posts
"""
def get_post(request, post_id):
    return HttpResponse("You're looking for post with id %s" % post_id)


def patch_post(request, post_id):
    return HttpResponse("You're looking to edit post with id %s" % post_id)


def post_post(request):
    return HttpResponse("You're posting a post!")


"""
Handling Users
"""
def post_user(request):
    return HttpResponse("You're posting a user!")


def get_user(request, user_id):
    return HttpResponse("You're requesting a user with id %s" % user_id)


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
