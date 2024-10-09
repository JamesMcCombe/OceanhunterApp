from django.contrib import admin
from .models import Page

class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'user', 'create', 'content')
    search_fields = ('title', 'slug', 'content')
    list_filter = ('status', 'create', 'publish')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If the object is being created, set the user
            obj.user = request.user
        super().save_model(request, obj, form, change)

admin.site.register(Page, PageAdmin)
