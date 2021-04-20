from django.contrib import admin

from .models import Pet 

@admin.register(Pet) # associate class with a model
class PetAdmin(admin.ModelAdmin):
    pass