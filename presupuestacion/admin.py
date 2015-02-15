from django.contrib import admin
from presupuestacion.models import *

class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('nombre',)}
admin.site.register(Proyecto,ProjectAdmin)
admin.site.register(Poste)
admin.site.register(Items)
admin.site.register(ItemPorPoste)
admin.site.register(UserProfile)