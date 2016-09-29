# from rest_framework import serializers
from rest_framework.serializers import (
							ModelSerializer, 
							HyperlinkedIdentityField,
							SerializerMethodField
						)

from accounts.api.serializers import UserDetailSerializer
from comments.api.serializers import CommentSerializer
from comments.models import Comment

from posts.models import Post

post_detail_url = HyperlinkedIdentityField(
			view_name='posts-api:detail',
			lookup_field='slug'
		)	

post_list_url = HyperlinkedIdentityField(
			view_name='posts-api:list',
			lookup_field='title'
		)	

""" Not necessary to create several serializers """


class PostCreateUpdateSerializer(ModelSerializer):           # class PostDetailSerializer(serializers.ModelSerializer):

	class Meta:
		model = Post
		fields = [
			'title',
			# 'slug',
			'content',
			'publish',
		]


class PostDetailSerializer(ModelSerializer):           # class PostDetailSerializer(serializers.ModelSerializer):

	url = post_detail_url
	# list_url = post_list_url
	# user = SerializerMethodField()
	user = UserDetailSerializer()
	image = SerializerMethodField()
	html = SerializerMethodField()
	comments = SerializerMethodField()
	class Meta:
		model = Post
		fields = [
			'url',
			# 'list_url',
			'user',
			'id',
			'title',
			'slug',
			'content',
			'html',
			'publish',
			'image',
			'comments',
		]

	def get_html(self, obj):
		return obj.get_markdown()

	# def get_user(self, obj):
	# 	return str(obj.user.username)


	def get_image(self, obj):
		try:
			image = obj.image.url
		except:
			image = None
		return image

	def get_comments(self, obj):
		# content_type = obj.get_content_type
		# object_id = obj.id
		c_qs = Comment.objects.filter_by_instance(obj)       # comment_queryset
		comments = CommentSerializer(c_qs, many=True).data
		return comments


class PostListSerializer(ModelSerializer):           # class PostListSerializer(serializers.ModelSerializer):

	url = HyperlinkedIdentityField(
			view_name='posts-api:detail',
			lookup_field='slug'
		)	

	# user = SerializerMethodField()
	user = UserDetailSerializer()
	class Meta:
		model = Post
		fields = [
			'url',
			'user',
			'id',
			'title',
			# 'slug',
			'content',
			'publish',
		]

	# def get_user(self, obj):
	# 	return str(obj.user.username)




# Serializing objects in the shell

"""
data = {
	'title': 'Programming Concepts',
	'slug': 'Programming-Concepts',
	'content': 'So here are the 5 basic concepts of any programming language:

    Variables.
    Control Structures.
    Data Structures.
    Syntax.
    Tools.',
    'publish': '2016-29-08'
}

new_item = PostSerializer(data=data)
print(new_item.initial_data)

if new_item.is_valid():
	new_item.save()
else:
	print(new_item.errors)


"""