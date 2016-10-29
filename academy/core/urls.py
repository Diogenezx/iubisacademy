from django.conf.urls import url
import academy.core.views


urlpatterns = [
	
    url (r'^$' , academy.core.views.home, name='home'),
    url (r'^dashboard' , academy.core.views.dash, name='dashboard'),
    url (r'^base' , academy.core.views.base, name='base'),
]