from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.db.models import Sum
from . import models as m


class ProfileInline(admin.StackedInline):
    exclude = ('gender', )
    model = m.Profile


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'profile_dob')
    inlines = (ProfileInline, )

    @admin.display(description='Date of Birth')
    def profile_dob(self, obj):
        return obj.profile.dob

admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'admin', 'total_points', 'create')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(total_points=Sum('users__fish__points'))
        return queryset

    @admin.display(description='Total points', ordering='total_points')
    def total_points(self, obj):
        return obj.total_points

admin.site.register(m.Team, TeamAdmin)


class InviteAdmin(admin.ModelAdmin):
    list_display = ('inviter', 'invitee', 'team', 'status', 'via', 'ref', 'create', 'key')

admin.site.register(m.Invite, InviteAdmin)
