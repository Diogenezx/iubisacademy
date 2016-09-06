from django.conf.urls import url, include
from django.contrib.auth.views import login as authLogin
from django.contrib.auth import logout
import academy.accounts.views


urlpatterns = [

	  url(r'^$', academy.accounts.views.show, name='show'),
   
    url(r'^entrar/$', authLogin, 
   		{'template_name': 'accounts/login.html'}, name='login'),
   
    url(r'^cadastre-se/', academy.accounts.views.register, name='register'),
    url(r'^nova-senha/', academy.accounts.views.password_reset, name='password_reset'),

    url(r'^sair/$', academy.accounts.views.Logout, name='logout'),
      	#{'next_page': 'core:home'}, name='logout'),
    url(r'^editar/$', academy.accounts.views.edit, name='edit'),  	
    url(r'^editar-senha/$', academy.accounts.views.edit_password, name='edit_password'), 
    

   ]