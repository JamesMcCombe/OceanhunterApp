from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db.models import Sum
from . import models as m


class ProfileInline(admin.StackedInline):
    exclude = ('gender', )
    model = m.Profile


class UserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_dob')
    inlines = (ProfileInline, )

    def profile_dob(self, obj):
        return obj.profile.dob

admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'total_points', 'create')

    def get_queryset(self, request):
        queryset = super(TeamAdmin, self).get_queryset(request)
        queryset = queryset.annotate(total_points=Sum('users__fish__points'))
        return queryset

    def total_points(self, obj):
        return obj.total_points
    total_points.short_description = 'Total points'
    total_points.admin_order_field = 'total_points'

admin.site.register(m.Team, TeamAdmin)


class InviteAdmin(admin.ModelAdmin):
    list_display = ('inviter', 'invitee', 'team', 'status', 'via', 'ref', 'create', 'key')

admin.site.register(m.Invite, InviteAdmin)
