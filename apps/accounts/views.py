from path import path
from os.path import abspath,dirname
from django.contrib.auth import get_user_model
from annoying.decorators import render_to
User = get_user_model()

APP_ROOT = path(dirname(abspath(__file__)))
APP_NAME = APP_ROOT.name

def T(name, ext='html'):
    return '{}/{}.{}'.format(APP_NAME, name, ext)

@render_to(T('index'))
def index(request):
    objs = User.objects.all()
    ctx = {'objs': objs}
    return ctx
