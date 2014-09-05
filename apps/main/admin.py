from django.contrib import admin
from . import models as m

class SpeciesAdmin(admin.ModelAdmin):
    list_display = ('name', 'k')

admin.site.register(m.Species, SpeciesAdmin)
