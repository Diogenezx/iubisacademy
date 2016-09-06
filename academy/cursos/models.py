from django.shortcuts import render, get_object_or_404
from django.db import models
from django.conf import settings
from academy.core.mail import send_mail_template


class CourseManager(models.Manager):

	def search(self, query):
		return self.get_queryset().all.filter(
			models.Q(name__icontains=query) | \
			models.Q(description__icontains=query)
			)

class Curso(models.Model):
	name = models.CharField('Nome', max_length=100)
	autor = models.CharField('Por', max_length=20, 
		blank=True
		)
	value = models.CharField('Valor' , max_length=15, blank=True)
	slug = models.SlugField('Slug')
	description = models.TextField('Descrição', blank=True)
	start_date = models.DateField(
		'Data de inicio', null=True, blank=True
		)
	image = models.ImageField(
		upload_to='cursos/images', verbose_name="Imagem",
		null=True, blank=True
		)


	created_at = models.DateTimeField(
		'Criado em', auto_now_add=True
		)
	updated_at = models.DateTimeField(
		'Atualizado em', auto_now=True
		)

	objects=CourseManager()
	def __str__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return('cursos:details', (), {'slug': self.slug})
		
	class Meta:
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering = ['-created_at']
		
class Enrollment(models.Model):
	
	STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'Cancelado'),
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, verbose_name='Usuário',
		related_name='enrollments'
		)		
	curso = models.ForeignKey(
		Curso, verbose_name='Curso', related_name='enrollments'
		)
	status = models.IntegerField('Situaçao', choices=STATUS_CHOICES, default=0,
		blank=True
		)

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField ('Atualizado em', auto_now=True)

	def active(self):
		self.status = 1
		self.save()

	def is_approved(self):
		return self.status == 1	

	class Meta:
		verbose_name = 'Inscrição'
		verbose_name_plural = 'Inscrições'
		unique_together = (('user', 'curso'),)

class Announcement(models.Model):

	curso = models.ForeignKey(
		Curso, verbose_name='Curso', related_name='announcements'
	)
	title = models.CharField('Título', max_length=100)
	content = models.TextField ('Conteúdo')

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField ('Atualizado em', auto_now=True)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Anúncio'
		verbose_name_plural = 'Anúncios'
		ordering = ['-created_at']

class Comment(models.Model):

	announcement =  models.ForeignKey(
		Announcement, verbose_name='Anúncio', related_name='comments'
	)	
	user = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Usuário')
	comment = models.TextField('Comentário')

	created_at = models.DateTimeField('Criado em', auto_now_add=True)
	updated_at = models.DateTimeField ('Atualizado em', auto_now=True)

	class Meta:
		verbose_name = 'Comentário'
		verbose_name_plural = 'Comentários'
		ordering = ['created_at']

def post_save_announcement(instance, created, **kwargs):
    if created:
        subject = instance.title
        context = {
            'announcement': instance
        }
        template_name = 'cursos/announcement_mail.html'
        enrollments = Enrollment.objects.filter(
            curso=instance.curso, status=1
        )
        for enrollment in enrollments:
            recipient_list = [enrollment.user.email]
            send_mail_template(subject, template_name, context, recipient_list)

models.signals.post_save.connect(
    post_save_announcement, sender=Announcement,
    dispatch_uid='post_save_announcement'
)		
