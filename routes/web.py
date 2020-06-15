"""Web Routes."""

from masonite.routes import Get, Post

ROUTES = [
    Get('/', 'WelcomeController@show').name('welcome'),
    Get('/hotels', 'HotelsController@show').name('hotels'),
]

from masonite.auth import Auth 
ROUTES += Auth.routes()
