from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .forms import ContactCourse, CommentForm
from .models import Curso, Enrollment, Announcement


def index(request):
		cursos = Curso.objects.all()
		template_name = 'cursos/index.html'
		context = {
			'cursos': cursos
		}
		return render(request, template_name, context)

def details(request, slug):
    curso = get_object_or_404(Curso, slug=slug)
    context = {
        'curso': curso
    }
    template_name = 'cursos/details.html'
    return render(request, template_name, context)

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
