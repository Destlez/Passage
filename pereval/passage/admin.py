from django.contrib import admin
from django.contrib.admin.templatetags.admin_list import admin_actions

from .models import User, Coordinates, Levels, Images, Passages

class PassagesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'coordinates', 'user', 'status')
    list_filter = ('title', 'user', 'add_time')


admin.site.register(Passages, PassagesAdmin)
admin.site.register(User)
admin.site.register(Coordinates)
admin.site.register(Levels)
admin.site.register(Images)
