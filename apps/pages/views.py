from django.shortcuts import render, get_object_or_404
from . import models as m

def page(request, slug):
    page = get_object_or_404(m.Page, slug=slug)
    ctx = {'page': page}
    return render(request, page.template, ctx)
