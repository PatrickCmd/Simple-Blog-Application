from django.conf.urls import url
# from . import views

from .views import (
		PostCreateAPIView,
		PostDeleteAPIView,
		PostListAPIView,
		PostDetailAPIView,
		PostUpdateAPIView,
		# post_detail,
		# post_update,
		# post_delete
	)

urlpatterns = [
	url(r'^$', PostListAPIView.as_view(), name="list"),       # class based views
	url(r'^create/$', PostCreateAPIView.as_view(), name="create"),
	url(r'^(?P<slug>[\w.@+-]+)/$', PostDetailAPIView.as_view(), name='detail'),
	url(r'^(?P<slug>[\w.@+-]+)/delete/$', PostDeleteAPIView.as_view(), name='delete'),
	url(r'^(?P<slug>[\w.@+-]+)/edit/$', PostUpdateAPIView.as_view(), name='update'),
]