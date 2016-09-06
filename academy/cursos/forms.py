from django import forms
from .models import Comment

class ContactCourse(forms.Form):

	name = forms.CharField(label='Nome', max_length=100)
	email = forms.EmailField(label='E-mail')
	message = forms.CharField(label='Mensagem/Dúvida', widget=forms.Textarea

)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['comment']
