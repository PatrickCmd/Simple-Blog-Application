from django.conf.urls import url

from .views import (
        CommentCreateAPIView,
        CommentDetailAPIView,
        # CommentEditAPIView,
        CommentListAPIView,
)

urlpatterns = [
	url(r'^$', CommentListAPIView.as_view(), name="list"),  # url(r'^$', post_list, name='list'),
    url(r'^create/$', CommentCreateAPIView.as_view(), name="create"),
	url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='comment_thread'),
    # url(r'^(?P<pk>\d+)/edit/$', CommentEditAPIView.as_view(), name='edit'),
	# url(r'^(?P<pk>\d+)/delete/$', views.confirm_delete, name='confirm_delete'),
	# url(r'^(?P<slug>[\w.@+-]+)/edit/$', views.comment_update, name='update'),
]