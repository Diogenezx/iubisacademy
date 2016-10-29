from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect



def home (request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/cursos')
	else:	
		return render(request, 'home.html')

def dash (request):
	return render(request, 'dashboard.html')

def base (request):
	return render(request, 'base.html')