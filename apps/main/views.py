
from annoying.decorators import render_to, ajax_request

from . import models as m

APP_NAME = 'main'


def T(t, ext='html'):
    return '{}/{}.{}'.format(APP_NAME, t, ext)


@render_to('home.html')
def home(request):
    return {}


@render_to('go.html')
def go(request):
    return {}
