from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.db import models
from django.conf import settings
from django.utils import timezone
from academy.core.mail import send_mail_template
from slugify import slugify
from datetime import date



class CourseManager(models.Manager):

	def search(self, query):
		return self.get_queryset().all.filter(
			models.Q(name__icontains=query) | \
			models.Q(description__icontains=query)
			)
#Categoria
class Categoria(models.Model):
	  
	name = models.CharField(
		max_length=100, 
		blank=False, 
		verbose_name="Categoria"
	)
	slug = models.SlugField(
		max_length=255, 
		blank=False, 
		verbose_name="Slug"
	)
	#categories = models.Manager()

	def __str__(self):
		return self.name

#Curso
class Curso(models.Model):
	name = models.CharField('Título', max_length=100, null=False)
	autor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=False)
	#autor = models.CharField(
	#	'Autor', max_length=20, blank=False, null=False, default="Equipe Iubis")
	
	VALORES = (
		('Grátis', 'Grátis'),
		('R$12', 'R$12'),
		('R$22', 'R$22'),
		('R$31', 'R$31'),
		('R$42', 'R$42'),
		('R$63', 'R$63'),
		('R$74', 'R$74'),
		('R$97', 'R$97'),
		('R$112', 'R$112'),
		('R$197', 'R$197'),
		('R$227', 'R$227'),
		('R$397', 'R$397'),
		('R$437', 'R$437'),
		('R$537', 'R$537'),
		('R$737', 'R$737'),
		('R$937', 'R$937'),
		('R$1197', 'R$1197'),
		('R$1997', 'R$1997'),
		('R$2997', 'R$2997'),
		('R$3997', 'R$3997'),
		('R$4997', 'R$4997'),

	)
	value = models.CharField(
		'Preço' , max_length=15, choices=VALORES, default='31', blank=True, null=True)
			
	slug = models.SlugField()
	description = models.TextField(
		'Descrição', blank=False, null=False
	)
	categoria = models.ForeignKey(
		Categoria, related_name="categories_tags", 
		blank=False, null=False
	)

	image = models.ImageField(
		upload_to='cursos/images', 
		verbose_name="Imagem do curso",
		null=True, 
		blank=True
	)
	image_capa = models.ImageField(
		upload_to='cursos/images/capa', 
		verbose_name="Capa do curso", 
		null=True, 
		blank=True
	)
	
	created_at = models.DateTimeField(
		'Criado em', auto_now_add=True
	)
	updated_at = models.DateTimeField(
		'Atualizado em', auto_now=True
	)
	objects=CourseManager()


	def save(self, *args, **kwargs):
		self.slug = slugify(self.name)
		super(Curso, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	@models.permalink
	def get_absolute_url(self):
		return('cursos:details', (), {'slug': self.slug})
	  
	def release_lessons(self):
		today = timezone.now().date()
		return self.lessons.filter(release_date__gte=today)

	class Meta:
		verbose_name = 'Curso'
		verbose_name_plural = 'Cursos'
		ordering = ['-created_at']	
#Aula
class Lesson(models.Model):

	name = models.CharField(
		'Título da aula', max_length=100
	)
	autor = models.ForeignKey(settings.AUTH_USER_MODEL, blank=False, null=True)
	description = models.TextField(
		'Descrição', blank=True
	)
	release_date = models.DateField(
		'Data de Liberação', 
		blank=True, 
		null=True, 
		default=date.today
	)
	curso = models.ForeignKey(
		Curso, verbose_name='Curso', 
		related_name='lessons',
	)
	

	created_at = models.DateTimeField(
		'Criado em', auto_now_add=True
	)
	updated_at = models.DateTimeField(
		'Atualizado em', auto_now=True
	)
	file = models.FileField(
		'Adicionar arquivo', 
		upload_to='lessons/materials', 
		blank=True, 
		null=True
	)
	#lesson = models.ForeignKey(Lesson, verbose_name='Aula', related_name='materials')

	def __str__(self):
		return self.name

	#Verificar se a aula está liberada	
	def is_available(self):
		if self.release_date:
			today = timezone.now().date()
			return self.release_date >= today
		return False

	#Ir para próxima aula	
	def get_next(self):
		next = Lesson.objects.filter(pk__gt=self.pk)
		if next:
			return next.first()
		return False
		
	#Voltar para aula anterior	
	def get_prev(self):
		prev = Lesson.objects.filter(pk__lt=self.pk).order_by('-pk')
		if prev:
			return prev.first()
		return False

	class Meta:
		verbose_name = 'Aula'
		verbose_name_plural = 'Aulas'
		ordering = ['created_at']

#Estado no curso (Inscrito ou não)		
class Enrollment(models.Model):
	
	STATUS_CHOICES = (
		(0, 'Pendente'),
		(1, 'Aprovado'),
		(2, 'Cancelado'),
	)
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		verbose_name='Usuário',
		related_name='enrollments'
	)		
	curso = models.ForeignKey(
		Curso, verbose_name='Curso', 
		related_name='enrollments'
	)
	status = models.IntegerField(
		'Status', choices=STATUS_CHOICES, 
		default=0, 
		blank=True
	)
	created_at = models.DateTimeField(
		'Criado em', auto_now_add=True
	)
	updated_at = models.DateTimeField(
		'Atualizado em', auto_now=True
	)

	def active(self):
		self.status = 1
		self.save()

	def pending(self):
		self.status = 0
		self.save()	

	def is_approved(self):
		return self.status == 1

	class Meta:
		verbose_name = 'Inscrição'
		verbose_name_plural = 'Inscrições'
		unique_together = (('user', 'curso'),)


#Anuncios
class Announcement(models.Model):

	curso = models.ForeignKey(
		Curso, verbose_name='Curso', 
		related_name='announcements'
	)
	title = models.CharField(
		'Título', max_length=100
	)
	content = models.TextField(
		'Conteúdo'
	)
	created_at = models.DateTimeField(
		'Criado em', auto_now_add=True
	)
	updated_at = models.DateTimeField(
		'Atualizado em', auto_now=True
	)

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = 'Anúncio'
		verbose_name_plural = 'Anúncios'
		ordering = ['-created_at']

#Comentários
class Comment(models.Model):

	announcement =  models.ForeignKey(
		Announcement, verbose_name='Anúncio', 
		related_name='comments'
	)	
	user = models.ForeignKey(
		settings.AUTH_USER_MODEL, 
		verbose_name='Usuário'
	)
	comment = models.TextField(
		'Comentário'
	)
	created_at = models.DateTimeField(
		'Criado em', auto_now_add=True
	)
	updated_at = models.DateTimeField(
		'Atualizado em', auto_now=True
	)

	class Meta:
		verbose_name = 'Comentário'
		verbose_name_plural = 'Comentários'
		ordering = ['created_at']

#Salvar anúncio e enviar email para os alunos
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

