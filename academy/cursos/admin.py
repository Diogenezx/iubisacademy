from django.contrib import admin

from .models import Curso, Enrollment, Announcement, Comment

class CourseAdmin(admin.ModelAdmin):

	list_display = ['name', 'slug', 'start_date', 'created_at']
	search_fields = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}
admin.site.register(Curso, CourseAdmin)
admin.site.register([Enrollment, Announcement, Comment])



