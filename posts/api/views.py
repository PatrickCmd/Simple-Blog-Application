from django.db.models import Q

from rest_framework.filters import (
							SearchFilter,
							OrderingFilter,
	                    )

from rest_framework.generics import	(
							CreateAPIView,
							DestroyAPIView,
							UpdateAPIView, 
							ListAPIView, 
							RetrieveAPIView,
							RetrieveUpdateAPIView
						) 

# from rest_framework.pagination import (
# 							LimitOffsetPagination,
# 							PageNumberPagination,
# 						)

from rest_framework.permissions import (
							AllowAny,
							IsAuthenticated,
							IsAdminUser,
							IsAuthenticatedOrReadOnly
						)

from posts.models import Post

from .pagination import PostLimitOffsetPagination, PostPageNumberPagination
from .permissions import IsOwnerOrReadOnly
from .serializers import PostCreateUpdateSerializer, PostDetailSerializer, PostListSerializer


class PostCreateAPIView(CreateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	# permission_classes = [IsAuthenticated]

	def perform_create(self, serializer):         # associating user wuth created post
		serializer.save(user=self.request.user)
	

class PostDetailAPIView(RetrieveAPIView):
	queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	# lookup_url_kwarg = 'abc'
	permission_classes = [AllowAny]

class PostUpdateAPIView(RetrieveUpdateAPIView):
	queryset = Post.objects.all()
	serializer_class = PostCreateUpdateSerializer
	lookup_field = 'slug'
	permission_classes = [IsOwnerOrReadOnly]
	# lookup_url_kwarg = 'abc'

	def perform_update(self, serializer):         # associating user wuth created post
		serializer.save(user=self.request.user)

class PostDeleteAPIView(DestroyAPIView):
	# queryset = Post.objects.all()
	serializer_class = PostDetailSerializer
	lookup_field = 'slug'
	# lookup_url_kwarg = 'abc'
	permission_classes = [IsOwnerOrReadOnly]


class PostListAPIView(ListAPIView):
	# queryset = Post.objects.all()
	serializer_class = PostListSerializer
	filter_backends = [SearchFilter, OrderingFilter]
	search_fields = ['title', 'content', 'user__first_name', 'user__last_name']

	# *******************Pagination**************************#
	# pagination_class = LimitOffsetPagination
	# pagination_class = PostLimitOffsetPagination

	# page pagination
	pagination_class = PostPageNumberPagination


	def get_queryset(self, *args, **kwargs):

		# queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
		queryset_list = Post.objects.all()
		search_query = self.request.GET.get('q')
		if search_query:
			queryset_list = queryset_list.filter(Q(title__icontains=search_query) |
												 Q(content__icontains=search_query) |
												 Q(user__first_name__icontains=search_query) |
												 Q(user__last_name__icontains=search_query)	
												).distinct()
		return queryset_list