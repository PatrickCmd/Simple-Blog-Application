from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models

# from posts.models import Post


class CommentManager(models.Manager):

	def all(self):
		qs = super(CommentManager, self).filter(parent=None)
		return qs    # filtering comments with no parent

	def filter_by_instance(self, instance):
		# content_type = ContentType.objects.get_for_model(Post)
		content_type = ContentType.objects.get_for_model(instance.__class__)
		obj_id = instance.id

		# filtering comments with no parent for reply
		qs = super(CommentManager, self).filter(content_type=content_type, object_id = obj_id).filter(parent=None)  
		# comments = Comment.objects.filter(content_type=content_type, object_id = obj_id)
		return qs

	def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
		model_qs = ContentType.objects.filter(model=model_type)
		if model_qs.exists():
			SomeModel = model_qs.first().model_class()  # eg Post Model
			obj_qs = SomeModel.objects.filter(slug=slug)
			if obj_qs.exists() and obj_qs.count() == 1:
				instance = self.model()
				instance.content = content
				instance.user = user
				instance.content_type = model_qs.first()
				instance.object_id = obj_qs.first().id
				if parent_obj:
					instance.parent = parent_obj
                instance.save()
                return instance
		return None

class Comment(models.Model):
	user       = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	# post       = models.ForeignKey(Post)

	content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id      = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	parent         =models.ForeignKey("self", null=True, blank=True)      # for referncing with reply

	content    = models.TextField()
	timestamp  = models.DateTimeField(auto_now_add=True)


	objects = CommentManager()


	def __unicode__(self):
		return str(self.user.username)

	def __str__(self):
		return str(self.user.username)

	# ordering comments descending
	class Meta:
		ordering = ["-timestamp"]

	def get_absolute_url(self):
		return reverse("comments:comment_thread", kwargs={"pk": self.pk})

	def get_delete_url(self):
		return reverse("comments:confirm_delete", kwargs={"pk": self.pk})


	def children(self):     # comment replies
		return Comment.objects.filter(parent=self)

	@property
	def is_parent(self):
		if self.parent is not None:
			return False
		return True
