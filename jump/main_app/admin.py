from django.contrib import admin

from jump.main_app.models import Equip, Photo, Spot


class EquipInlineAdmin(admin.StackedInline):
    model = Equip


@admin.register(Equip)
class EquipAdmin(admin.ModelAdmin):
    list_display = ('brand', 'type')


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    pass


@admin.register(Spot)
class SpotAdmin(admin.ModelAdmin):
    pass
