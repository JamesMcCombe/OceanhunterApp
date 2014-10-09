from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from . import models as m

class ProfileInline(admin.StackedInline):
    model = m.Profile

class UserAdmin(UserAdmin):
        inlines = (ProfileInline, )

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'kind', 'admin', 'points', 'create')

admin.site.register(m.Team, TeamAdmin)


class InviteAdmin(admin.ModelAdmin):
    list_display = ('inviter', 'invitee', 'team', 'status', 'via', 'ref', 'create')

admin.site.register(m.Invite, InviteAdmin)
