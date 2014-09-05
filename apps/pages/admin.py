from django.contrib import admin
from . import models as m

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'create', 'content')

admin.site.register(m.Page, PageAdmin)
