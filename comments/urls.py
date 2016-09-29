from django.conf.urls import url

from . import views

# from .views import (
# 		comment_list,
# 		comment_create,
# 		comment_thread,
# 		comment_update,
# 		comment_delete
# 	)

urlpatterns = [
	# url(r'^$', views.comment_list, name="list"),  # url(r'^$', post_list, name='list'),
	# url(r'^create/$', views.comment_create),
	url(r'^(?P<pk>\d+)/$', views.comment_thread, name='comment_thread'),
	url(r'^(?P<pk>\d+)/delete/$', views.confirm_delete, name='confirm_delete'),
	# url(r'^(?P<slug>[\w.@+-]+)/edit/$', views.comment_update, name='update'),
]