from __future__ import unicode_literals

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.signals import pre_save
from django.core.urlresolvers import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from markdown_deux import markdown

from comments.models import Comment
from .utils import get_read_time

# model Manager
# Post.objects.all()
# Post.objects.create(user, title="mmm")

class PostManager(models.Manager): 
	def active(self, *args, **kwargs):      # all or active
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(instance, filename):
	return "%s/%s" %(instance, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
	title = models.CharField(max_length=120)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location,
								 null=True, blank=True,
								 width_field = "width_field",
								 height_field = "height_field"
								 )
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	read_time = models.TimeField(null=True, blank=True)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager()    # instantiating the object Manager


	def __unicode__(self):
		return self.title


	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"slug": self.slug})    # return reverse("posts:detail", kwargs={"slug": self.slug})
		# return "/posts/%s/" %(self.id)

	def get_api_url(self):
		return reverse("posts-api:detail", kwargs={"slug": self.slug})

	def get_edit_url(self):
		return reverse("posts:update", kwargs={"slug": self.slug})

	def get_delete_url(self):
		return reverse("posts:delete", kwargs={"slug": self.slug})


	class Meta:  # ordering Posts 
		ordering = ["-timestamp", "-updated"]

	# markdown rendering using markdown_deux
	def get_markdown(self):
		content = self.content
		marked_text = markdown(content)
		return mark_safe(marked_text)

	@property           # post comments
	def comments(self):
		instance = self
		qs = Comment.objects.filter_by_instance(instance)
		return qs

	@property           # post comments create
	def get_content_type(self):
		instance = self
		content_type = ContentType.objects.get_for_model(instance.__class__)
		return content_type

def create_slug(instance, new_slug=None):
	slug = slugify(instance.title)
	if new_slug is not None:
		slug = new_slug
	qs = Post.objects.filter(slug=slug).order_by("-id")
	exists = qs.exists()

	if exists:
		new_slug = "%s-%s" %(slug, qs.first().id)
		return create_slug(instance, new_slug=new_slug)
	return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    # slug = slugify(instance.title)

    # exists = Post.objects.filter(slug=slug).exists()

    # if exists:
    # 	slug = "%s-%s" %(slug, instance.id)
    # instance.slug = slug

    if not instance.slug:
    	instance.slug = create_slug(instance)

    if instance.content:
    	html_string = instance.get_markdown()
    	read_time_variable = get_read_time(html_string)
    	instance.read_time = read_time_variable


pre_save.connect(pre_save_post_receiver, sender=Post)