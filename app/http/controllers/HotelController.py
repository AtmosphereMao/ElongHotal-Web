"""A HotelController Module."""

from masonite.request import Request
from masonite.view import View
from masonite.controllers import Controller
import ehotal


class HotelController(Controller):
    """HotelController Controller Class."""

    def __init__(self, request: Request):
        """HotelController Initializer

        Arguments:
            request {masonite.request.Request} -- The Masonite Request class.
        """
        self.request = request

    def show(self, view: View):
        hotelId = self.request.param('hotelId')
        hotelDiv = ehotal.getHotel(hotelId)
        return view.render('hotelView', {'hotelIntroduce':hotelDiv['hotelIntroduce'], 'hotelInfo': hotelDiv['hotelInfo']})