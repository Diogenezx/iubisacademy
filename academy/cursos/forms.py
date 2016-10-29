import itertools
from django import forms
from django.utils.text import slugify
from .models import Comment, Curso, Lesson
from django.forms.widgets import HiddenInput


class addLessonForm(forms.ModelForm):
	
	class Meta:
		model = Lesson
		fields = ['name', 'description', 'release_date', 'curso' , 'file']
		widgets={
					"curso": forms.HiddenInput(),
					"release_date":forms.DateInput(attrs={'class':'datepicker','placeholder':'dd/mm/aaaa'}),
					"description":forms.Textarea(attrs={'class':'materialize-textarea', 'placeholder':'Descrição da aula'}),
					"name":forms.TextInput(attrs={'autofocus': 'autofocus', 'placeholder':'Nome da aula'})

					
				}
	
	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	self.fields['curso'].initial =  50 #Valor para ser preenchido
	# 	curso=forms.Select()

class add_course(forms.ModelForm):
	
	class Meta:
		model = Curso
		fields = ['name', 'value', 'description', 'categoria', 'image']
		widgets={
					  "name":forms.TextInput(attrs={'placeholder':'Título do curso'}),
					  "description":forms.Textarea(attrs={'placeholder':'Descrição do curso', 'class':'materialize-textarea'}),
					  "value":forms.Select(attrs={'placeholder':'Preço do curso'}),
					  "image":forms.FileInput(attrs={'class':'file-field input-field', 'type':'file'}),
					  "categoria":forms.Select(attrs={'class':'input-field'}),

				  }	  
			   
class ContactCourse(forms.Form):

	name = forms.CharField(label='Nome', max_length=100)
	email = forms.EmailField(label='E-mail')
	message = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea)

class CommentForm(forms.ModelForm):

	class Meta:
		model = Comment
		fields = ['comment']