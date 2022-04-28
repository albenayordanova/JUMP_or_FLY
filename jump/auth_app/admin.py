from django.contrib import admin

from jump.auth_app.models import Profile, JumpUser


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # inlines = (EquipInlineAdmin,)
    list_display = ('first_name', 'last_name')


@admin.register(JumpUser)
class JumpUserAdmin(admin.ModelAdmin):
    pass
