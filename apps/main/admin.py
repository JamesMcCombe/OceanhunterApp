from django.contrib import admin
from apps.main.models import Division, Species, Fish, Comment

class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'base')  #, 'k')

admin.site.register(Species, SpeciesAdmin)

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

class FishAdmin(admin.ModelAdmin):
    list_display = ('user', 'species', 'weight', 'witness', 'points', 'create')
    inlines = (CommentInline, )

admin.site.register(Fish, FishAdmin)


class DivisionAdmin(admin.ModelAdmin):
    filter_horizontal = ('species', )
admin.site.register(Division, DivisionAdmin)
