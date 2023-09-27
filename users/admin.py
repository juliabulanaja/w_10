from django.contrib import admin
from django.contrib.auth.models import User

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    # list_display = ('username', 'first_name', 'last_name', 'email')
    fields = ['username', 'first_name', 'last_name', 'password', 'email']
admin.site.unregister(User)
admin.site.register(User, UserAdmin)
