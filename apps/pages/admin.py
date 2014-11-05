from django.contrib import admin
from . import models as m

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'create', 'content')

    def save_model(self, request, obj, form, change):
        u = request.user
        obj.user = u
        obj.save()

admin.site.register(m.Page, PageAdmin)
