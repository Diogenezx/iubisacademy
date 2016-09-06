from django.conf.urls import url, include
import academy.core.views

urlpatterns = [
	
    url (r'^$' , academy.cursos.views.index, name='index'),
   #url (r'^(?P<pk>\d+)/$' , academy.cursos.views.details, name='details'),
    url (r'^(?P<slug>[\w_-]+)/$', academy.cursos.views.details, name='details'),
   	url (r'^(?P<slug>[\w_-]+)/inscricao/$', academy.cursos.views.enrollment, name='enrollment'),
   	url (r'^(?P<slug>[\w_-]+)/anuncios/$', academy.cursos.views.announcements, name='announcements'),
   	url(r'^(?P<slug>[\w_-]+)/anuncios/(?P<pk>\d+)/$', academy.cursos.views.show_announcement, name='show_announcement'),
   	url (r'^(?P<slug>[\w_-]+)/cancelar-inscricao/$', academy.cursos.views.undo_enrollment, name='undo_enrollment'),



]
