from django.shortcuts import render, get_object_or_404
from apps.pages.models import Page

def page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    ctx = {'page': page}
    return render(request, page.template, ctx)
