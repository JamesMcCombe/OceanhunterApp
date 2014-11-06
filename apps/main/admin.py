from django.contrib import admin
from . import models as m

class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'base', 'k')

admin.site.register(m.Species, SpeciesAdmin)

class CommentInline(admin.StackedInline):
    model = m.Comment
    extra = 1

class FishAdmin(admin.ModelAdmin):
    list_display = ('user', 'species', 'weight', 'witness', 'points', 'create')
    inlines = (CommentInline, )

admin.site.register(m.Fish, FishAdmin)
