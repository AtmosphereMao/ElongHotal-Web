"""A HotelsController Module."""

from masonite import env
from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
import ehotal


class HotelsController(Controller):
    """HotelsController Controller Class."""

    def __init__(self, request: Request):
        """HotelsController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View):
        pageNo = self.request.input('page')
        sort = self.request.input('sort') if self.request.input('sort') else 0
        keyword = self.request.input('keyword') if self.request.input('keyword') else ''

        if pageNo == False:
            return self.request.redirect(env('APP_URL')+"/hotels?page=1&sort=0&keyword=")


        data = ehotal.getHotels(page=int(pageNo), sort=int(sort), keyword=keyword)
        hotels = data['data']['hotelList']
        pages = data['data']['page']
        return view.render('hotelsView', {'hotelsList': hotels, 'pages': pages})
