from django.shortcuts import render, get_object_or_404
from .models import Page

def page(request, slug):
    page = get_object_or_404(Page, slug=slug)
    context = {'page': page}
    return render(request, page.template, context)
