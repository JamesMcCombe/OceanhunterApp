from django.contrib import admin
from . import models as m

class UserAdmin(admin.ModelAdmin):
    list_display = ('username',)

admin.site.register(m.User,UserAdmin)
