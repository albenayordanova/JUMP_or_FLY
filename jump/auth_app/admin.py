from django.contrib import admin

from jump.auth_app.models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # inlines = (EquipInlineAdmin,)
    list_display = ('first_name', 'last_name')
