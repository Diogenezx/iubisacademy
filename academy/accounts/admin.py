from django.contrib import admin

from .models import User

class CourseAdmin(admin.ModelAdmin):

	list_display = ['name', 'email', 'image', 'is_staff']
	search_fields = ['name', 'email']

admin.site.register(User, CourseAdmin)



