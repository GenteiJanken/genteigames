from games.models import *
from django.contrib import admin

class GameResourceInline(admin.TabularInline):
    model = GameResource
    extra = 2

class GameAdmin(admin.ModelAdmin):
    inlines = [
        GameResourceInline,
    ]

admin.site.register(Game, GameAdmin)
admin.site.register(GameResource)
