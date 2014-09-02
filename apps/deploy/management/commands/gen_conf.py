from django.core.management.base import NoArgsCommand
from django.template.loader import render_to_string as r2s
from django.conf import settings

def render(template,outname):
    s = r2s(template,{'settings':settings})
    p = settings.PROJ_ROOT/outname
    p.write_text(s)
    print outname
    print '-' * 30
    print s

def link(outname,linkname,destination):
    outpath = settings.PROJ_ROOT/outname
    return 'cd %s & ln -is %s %s' % (destination,outpath,outname)

class Command(NoArgsCommand):
    help = 'generate conf files'

    def handle_noargs(self,**options):

        template = 'nginx.conf'
        outname = '%s.conf' % settings.PROJ_NAME
        render(template,outname)

        template = 'uwsgi.ini'
        outname = '%s.ini' % settings.PROJ_NAME
        render(template,outname)

        template = 'install.sh'
        outname = template
        render(template,outname)
