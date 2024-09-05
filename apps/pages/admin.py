from django.contrib import admin
from . import models as m

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'create', 'content')

    def save_model(self, request, obj, form, change):
        if not obj.user_id:
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(m.Page, PageAdmin)
