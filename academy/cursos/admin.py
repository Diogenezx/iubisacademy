from django.contrib import admin

from .models import Curso, Enrollment, Announcement, Comment, Categoria, Lesson

class LessonAdmin(admin.StackedInline):

	model = Lesson

class CourseAdmin(admin.ModelAdmin):

	list_display = ['name', 'slug', 'categoria', 'created_at']
	search_fields = ['name', 'slug']
	prepopulated_fields = {'slug': ('name',)}

	inlines = [LessonAdmin,]
	

admin.site.register(Curso, CourseAdmin)
admin.site.register(Categoria)
admin.site.register([Enrollment, Announcement, Comment])
#admin.site.register(Lesson, LessonAdmin)


