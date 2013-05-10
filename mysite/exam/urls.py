from django.conf.urls import patterns, url

from exam import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^firstImage',views.show_first_image),

)


