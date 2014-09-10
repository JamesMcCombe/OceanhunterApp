from django.contrib import admin
from . import models as m

class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'k')

admin.site.register(m.Species, SpeciesAdmin)

class FishAdmin(admin.ModelAdmin):
    list_display = ('user', 'species', 'weight', 'witness', 'create')

admin.site.register(m.Fish, FishAdmin)
