from django.template import Library

register = Library()

from academy.cursos.models import Enrollment

@register.inclusion_tag('cursos/templatetags/my_courses.html')
def my_courses(user):
	enrollments = Enrollment.objects.filter(user=user)
	context = {
		'enrollments': enrollments
	}
	return context


@register.assignment_tag
def load_my_courses(user):
	return Enrollment.objects.filter(user=user)	