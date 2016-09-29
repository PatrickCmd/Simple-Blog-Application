from django.db.models import Q

from rest_framework.filters import (
    SearchFilter,
    OrderingFilter,
)

from rest_framework.mixins import DestroyModelMixin, UpdateModelMixin

from rest_framework.generics import (
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

from posts.api.pagination import PostLimitOffsetPagination, PostPageNumberPagination
from posts.api.permissions import IsOwnerOrReadOnly

from comments.models import Comment

from .serializers import (
    CommentSerializer,
    CommentDetailSerializer,
    # CommentEditSerializer,
    CommentListSerializer,
    create_comment_serializer
    )


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    # serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        model_type = self.request.GET.get("type")
        slug = self.request.GET.get("slug")
        parent_id = self.request.GET.get("parent_id", None)

        return create_comment_serializer(
            model_type=model_type,
            slug=slug,
            parent_id=parent_id,
            user=self.request.user
        )

    # def perform_create(self, serializer):  # associating user wuth created post
    #     serializer.save(user=self.request.user)


# class CommentDetailAPIView(RetrieveAPIView):
#     queryset = Comment.objects.all()
#     serializer_class = CommentDetailSerializer
#     lookup_field = 'pk'
#     # lookup_url_kwarg = 'abc'


class CommentDetailAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
    queryset = Comment.objects.filter(id__gte=0)
    serializer_class = CommentDetailSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

# class CommentEditAPIView(DestroyModelMixin, UpdateModelMixin, RetrieveAPIView):
#     queryset = Comment.objects.filter(id__gte=0)
#     serializer_class = CommentEditSerializer
#
#     def put(self, request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)
#
#     def delete(self, request, *args, **kwargs):
#         return self.delete(request, *args, **kwargs)

# class PostUpdateAPIView(RetrieveUpdateAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostCreateUpdateSerializer
#     lookup_field = 'slug'
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
#
#     # lookup_url_kwarg = 'abc'
#
#     def perform_update(self, serializer):  # associating user wuth created post
#         serializer.save(user=self.request.user)


# class PostDeleteAPIView(DestroyAPIView):
#     # queryset = Post.objects.all()
#     serializer_class = PostDetailSerializer
#     lookup_field = 'slug'
#     # lookup_url_kwarg = 'abc'
#     permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


class CommentListAPIView(ListAPIView):
    # queryset = Post.objects.all()
    serializer_class = CommentListSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['content', 'user__first_name', 'user__last_name']
    permission_classes = [IsAuthenticated]

    # *******************Pagination**************************#
    # pagination_class = LimitOffsetPagination
    # pagination_class = PostLimitOffsetPagination

    # page pagination
    pagination_class = PostPageNumberPagination

    def get_queryset(self, *args, **kwargs):
        # queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        # queryset_list = Comment.objects.all()
        queryset_list = Comment.objects.filter(id__gte=0)
        search_query = self.request.GET.get('q')
        if search_query:
            queryset_list = queryset_list.filter(Q(content__icontains=search_query) |
                                                 Q(user__first_name__icontains=search_query) |
                                                 Q(user__last_name__icontains=search_query)
                                                 ).distinct()
        return queryset_list
