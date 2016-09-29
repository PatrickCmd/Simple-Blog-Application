from django.conf.urls import url

from . import views

# from .views import (
# 		post_list,
# 		post_create,
# 		post_detail,
# 		post_update,
# 		post_delete
# 	)

urlpatterns = [
	url(r'^$', views.post_list, name="list"),  # url(r'^$', post_list, name='list'),
	url(r'^create/$', views.post_create, name="create"),
	url(r'^(?P<slug>[\w-]+)/$', views.post_detail, name='detail'),
	url(r'^(?P<slug>[\w-]+)/delete/$', views.post_delete, name='delete'),
	url(r'^(?P<slug>[\w-]+)/edit/$', views.post_update, name='update'),
]