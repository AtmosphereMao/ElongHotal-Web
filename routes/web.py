"""Web Routes."""

from masonite.routes import Get, Post

ROUTES = [

    Get('/home', 'WelcomeController@show').name('home'),
    Get('/', 'WelcomeController@show').name('welcome'),
    Get('/hotels', 'HotelsController@show').name('hotels'),
    Get('/hotels/@hotelId', 'HotelController@show').name('hotel'),
]

# from masonite.auth import Auth
# ROUTES += Auth.routes()
