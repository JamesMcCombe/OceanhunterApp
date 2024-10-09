from django.contrib import admin
from apps.main.models import Division, Species, Fish, Comment

class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'base')

admin.site.register(Species, SpeciesAdmin)

class CommentInline(admin.StackedInline):
    model = Comment
    extra = 1

class FishAdmin(admin.ModelAdmin):
    list_display = ('user', 'species', 'weight', 'witness', 'points', 'create')
    inlines = [CommentInline]

admin.site.register(Fish, FishAdmin)

class DivisionAdmin(admin.ModelAdmin):
    list_display = ('name', 'species_list')
    filter_horizontal = ('species',)

    def species_list(self, obj):
        return ', '.join([s.name for s in obj.species.all()])

admin.site.register(Division, DivisionAdmin)
