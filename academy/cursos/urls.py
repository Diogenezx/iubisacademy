from django.conf.urls import url, include
from django.conf.urls.static import static
from django.conf import settings


import academy.core.views
urlpatterns = [
    
    url(r'^$', academy.cursos.views.index, name='index'),
    url(r'^dashboard/$', academy.cursos.views.dashboard_in, name='dashboard_in'),
    url(r'^produtor/$', academy.cursos.views.addCourse, name='addCourse'),
    url(r'^painel-aula/(?P<slug>[\w_-]+)$', academy.cursos.views.addLesson, name='addLesson'),
    url(r'^editar-aula/$', academy.cursos.views.LessonUpdate, name='LessonUpdate'),
    url(r'^editar-curso/(?P<id>\d+)/$', academy.cursos.views.CursoUpdate.as_view(), name='CursoUpdate'),
    url(r'^apagar/(?P<pk>.*)$', academy.cursos.views.delete_course, name='delete_course'),
    url(r'^(?P<slug>[\w_-]+)/$', academy.cursos.views.details, name='details'),
    url(r'^(?P<slug>[\w_-]+)/inscricao/$', academy.cursos.views.enrollment, name='enrollment'),
    url(r'^(?P<slug>[\w_-]+)/anuncios/$', academy.cursos.views.announcements, name='announcements'),
    url(r'^(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)/$', academy.cursos.views.show_announcement, name='show_announcement'),
    url(r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$', academy.cursos.views.undo_enrollment, name='undo_enrollment'),
    url(r'^(?P<slug>[\w_-]+)/aulas/$', academy.cursos.views.lessons, name='lessons'),
    url(r'^(?P<slug>[\w_-]+)/aulas/(?P<pk>\d+)/$', academy.cursos.views.lesson, name='lesson'),

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
