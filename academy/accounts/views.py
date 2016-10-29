from django.shortcuts import render, redirect
from django.conf.urls import url
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm 
from django.conf import settings
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

from academy.cursos.models import Enrollment
from academy.core.utils import generate_hash_key
from .forms import RegisterForm, EditAccountForm, PasswordResetForm
from .models import PasswordReset

User = get_user_model()


#Mostra cursos que está inscrito
@login_required
def show (request):
		template_name = 'accounts/show.html'
		context = {}
		context['enrollments'] = Enrollment.objects.filter(user=request.user)
		return render (request, template_name, context)	

 # class Meta:
 #        permissions = (
 #            ('pode_mudar_status', 'Pode mudar status'),
 #            ('pode_fazer_outra_coisa', 'Pode fazer outra coisa'),
 #        )		

#Página de registro (cadastro)
def register(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/cursos')
	else:	
		template_name = 'accounts/register.html'
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			user = form.save()
			user = authenticate(
				username=user.username, password=form.cleaned_data['password1']
				)
			login(request, user)
			return redirect  ('cursos:index')
		
	else: 
		form =  RegisterForm()		
	context = {
		'form': form
	}
	return render (request, template_name, context)

#Página para resetar a senha
def password_reset(request):
	template_name = 'accounts/password_reset.html'
	context = {}
	form = PasswordResetForm(request.POST or None)
	if form.is_valid():
		form.save()
		context['success'] = True
	context['form'] = form	 
	return render(request, template_name, context)

#Saida da conta
def Logout(request):
	logout(request)
	return redirect ('core:home')

#Página para editar conta
@login_required
def edit (request):
	template_name = 'accounts/edit.html'
	form = EditAccountForm()
	context = {}
	if request.method == 'POST':
		form = EditAccountForm(request.POST, instance=request.user)
		if form.is_valid():
			form.save()
			context['success'] = True
		
	else: 
		form =  EditAccountForm()		
	context = {
		'form': form
	}
	context['form'] = form
	return render (request, template_name, context)

#Página para editar senha (alterar)
@login_required
def edit_password(request):
	template_name = 'accounts/edit_password.html'
	context = {}
	if request.method == 'POST':
		form = PasswordChangeForm(data= request.POST, user=request.user)
		if form.is_valid():
			form.save()
			context['success'] = True
	else:
		form = PasswordChangeForm(user=request.user)
	context['form'] = form
	return render (request, template_name, context)


