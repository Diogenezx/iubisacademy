from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
from django.core.urlresolvers import reverse



from .decorators import enrollment_required
from .forms import ContactCourse, CommentForm, add_course, addLessonForm
from .models import Curso, Enrollment, Announcement, Lesson, Categoria
from django.views.generic import UpdateView



#Exibe os cursos na página inicial e efetua a pesquisa
def index(request):
	cursos = Curso.objects.all()
	query = request.GET.get("q")
	if query:
		cursos = cursos.filter(
			models.Q(name__icontains=query) |
			models.Q(description__icontains=query)
			).distinct()
		# models.Q(autor__icontains=query)

	template_name = 'cursos/index.html'
	context = {
		'cursos': cursos
	}
	return render(request, template_name, context)


#Página de detalhes sobre o curso
def details(request, slug):
	curso = get_object_or_404(Curso, slug=slug)
	context = {
		'curso': curso
	}
	template_name = 'cursos/details.html'
	return render(request, template_name, context)


#Se inscreve no curso
@login_required
def enrollment(request, slug):
	curso = get_object_or_404(Curso, slug=slug)
	enrollment, created = Enrollment.objects.get_or_create(
		user=request.user, curso=curso
	)
	if created:
		enrollment.active()
		messages.success(request, 'Você foi inscrito no curso com sucesso')
	else:
		messages.info(request, 'Você já está inscrito no curso')
	return redirect('accounts:show')


#Sair do curso
@login_required
def undo_enrollment(request, slug):
	curso = get_object_or_404(Curso, slug=slug)
	enrollment = get_object_or_404(
		Enrollment, user=request.user, curso=curso
	)
	if request.method == 'POST':
		enrollment.delete()
		messages.success(request, 'Sua inscrição foi cancelada com sucesso')
		return redirect('accounts:show')
	template = 'cursos/undo_enrollment.html'
	context = {
		'enrollment': enrollment,
		'curso': curso,
	}
	return render(request, template, context)


#Cria um novo anúncio (produtor para alunos)
@login_required
def announcements(request, slug):
	curso = get_object_or_404(Curso, slug=slug)
	if not request.user.is_staff:
		enrollment = get_object_or_404(
			Enrollment, user=request.user, curso=curso
		)
		if not enrollment.is_approved():
			messages.error(request, 'Inscrição pendente')
			return redirect('accounts:show')
	template = 'cursos/announcements.html'
	context = {
		'curso': curso,
		'announcements': curso.announcements.all()
	}
	return render(request, template, context)


#Mostra os anúncios e verifica comentários
@login_required
def show_announcement(request, slug, pk):
	curso = get_object_or_404(Curso, slug=slug)
	if not request.user.is_staff:
		enrollment = get_object_or_404(
			Enrollment, user=request.user, curso=curso
		)
		if not enrollment.is_approved():
			messages.error(request, 'A sua inscrição está pendente')
			return redirect('accounts:dashboard')
	announcement = get_object_or_404(curso.announcements.all(), pk=pk)
	form = CommentForm(request.POST or None)
	if form.is_valid():
		comment = form.save(commit=False)
		comment.user = request.user
		comment.announcement = announcement
		comment.save()
		form = CommentForm()
		messages.success(request, 'Seu comentário foi enviado com sucesso')
	template = 'cursos/show_announcement.html'
	context = {
		'curso': curso,
		'announcement': announcement,
		'form': form,
	}
	return render(request, template, context)


#Listagem das aulas e validação
@login_required
@enrollment_required
def lessons(request, slug):
	curso = request.curso
	template = 'cursos/lessons.html'
	lessons = curso.release_lessons()
	if request.user.is_staff:
		lessons = curso.lessons.all()
	context = {
		'curso': curso,
		'lessons': lessons
	}
	return render(request, template, context)



#Aula individual e validação
@login_required
@enrollment_required
def lesson(request, slug, pk):
	curso = request.curso
	lesson = get_object_or_404(Lesson, pk=pk, curso=curso)
	if not request.user.is_staff and not lesson.is_available():
		messages.error(request, 'Esta aula não está disponível')
		return redirect('cursos:lessons', slug=curso.slug)
	template = 'cursos/lesson.html'
	context = {
		'curso': curso,
		'lesson': lesson
	}
	return render(request, template, context)

#######################################
#  Funcionalidades painel do produtor #
#######################################


#Dashboard conteúdo produtor
@login_required
def dashboard_in(request):
	cursos = Curso.objects.filter(autor=request.user)
	template_name = 'assets/dashboard_2.html'
	context = {
		'cursos':cursos,
		
	}
	
	return render(request, template_name, context)
#Adicionar aulas painel produtor

@login_required
def addLesson(request, slug):
	curso = get_object_or_404(Curso, slug=slug)
	if request.method == 'POST':
		form = addLessonForm(request.POST, request.FILES, initial={'curso': curso.id})
		if form.is_valid():
			obj = form.save(commit=False)
			obj.field1 = request.user
			obj.save()
			messages.success(request, 'Aula adicionada com sucesso')
		return redirect('cursos:dashboard_in')
	else: 
		form = addLessonForm(initial={'curso': curso.id})
	template_name = 'cursos/addLesson.html'
	context = { 
		'form': form,
		'curso':curso,
	}

	return render(request, template_name, context)



#Add Course
@login_required
def addCourse(request):
	if request.method == 'POST':
		form = add_course(request.POST, request.FILES)
		if form.is_valid():
			curso = Curso()
			curso.autor = request.user
			curso.value = form.cleaned_data['value']
			curso.name = form.cleaned_data['name']
			curso.description = form.cleaned_data['description']
			curso.categoria = form.cleaned_data['categoria']
			curso.image = form.cleaned_data['image']
			curso.save()
			return redirect('cursos:index')
	else:
		form = add_course()

	template_name = 'cursos/new_course.html'	
	context = {
		'form': form
	}    

	return render(request, template_name, context)
	
@login_required	
def delete_course (request, pk):
	query = Curso.objects.get(pk=pk)
	query.delete()
	return redirect('cursos:dashboard')


def LessonUpdate(request):
	curso = Curso.objects.all()
	template_name = 'cursos/edit-lesson.html'
	context = {
		'lesson': curso,
	}
	return render(request, template_name, context)

#Editar informações do curso		
class CursoUpdate(UpdateView):
	form_class = add_course	
	model = Curso
	template_name = 'cursos/edit.html'

	
	def dispatch(self, request, *args, **kwargs):
	# Try to dispatch to the right method; if a method doesn't exist,
	# defer to the error handler. Also defer to the error handler if the
	# request method isn't on the approved list.
		if request.method.lower() in self.http_method_names:
			handler = getattr(self, request.method.lower(), self.http_method_not_allowed)
		else:
			handler = self.http_method_not_allowed
		self.request = request
		self.args = args
		self.kwargs = kwargs
		return handler(request, *args, **kwargs)

	def get_object(self, queryset=None):
		obj = Curso.objects.get(id=self.kwargs['id'])
		return obj