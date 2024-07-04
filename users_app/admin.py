from django.contrib import admin
from .models import CustomUser, CustomUserConfirmation, Note
from django.contrib.auth.models import Group


class CustomUserAdmin(admin.ModelAdmin):
    # list_editable = ['first_name', 'last_name', 'phone_number']
    list_display = ['username', 'auth_status', 'phone_number', 'auth_type', 'province']

class CustomUserConfirmationAdmin(admin.ModelAdmin):
    # list_editable = ['code', 'expiration_time', 'is_confirmed',]
    list_display = ('user', 'verify_type', 'code', 'expiration_time', 'is_confirmed', 'created_time')
        
class NoteAdmin(admin.ModelAdmin):
    # list_editable = ['code', 'expiration_time', 'is_confirmed',]
    list_display = ('text', 'owner', 'created_time', 'updated_time')


admin.site.unregister(Group)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(CustomUserConfirmation, CustomUserConfirmationAdmin)
admin.site.register(Note, NoteAdmin)

