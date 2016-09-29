from urllib import quote_plus
from django.contrib import messages
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from comments.forms import CommentForm
from comments.models import Comment
from .models import Post
from .forms import PostForm
from .utils import get_read_time

def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active()   # using model Manger
	if request.user.is_staff or request.user.is_superuser:
	    queryset_list = Post.objects.all() # .order_by("-timestamp")	
	# queryset_list = Post.objects.filter(draft=False).filter(publish__lte=timezone.now())

	search_query = request.GET.get('q')
	if search_query:
		queryset_list = queryset_list.filter(Q(title__icontains=search_query) |
											 Q(content__icontains=search_query) |
											 Q(user__first_name__icontains=search_query) |
											 Q(user__last_name__icontains=search_query)	
											).distinct()

	paginator = Paginator(queryset_list, 4) # Show 10 queryset per page

	page = request.GET.get('page')
	try:
		queryset = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer, deliver first page.
		queryset = paginator.page(1)
	except EmptyPage:
		# If page is out of range (e.g. 9999), deliver last page of results.
		queryset = paginator.page(paginator.num_pages)

	context ={
		"object_list": queryset,
		"title": "Post Lists",
		"today": today,
	}
	return render(request, 'posts/post_list.html', context)	
	

def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:     # if not user cannot create, update or delete post
		raise Http404
	
	# if not request.user.is_authenticated():
	# 	raise Http404

	# instance = Post.objects.get(pk=3)
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		print(form.cleaned_data.get("title"))
		instance = form.save()
		# message sucess
		messages.success(request, "Post Successfully created")
		return HttpResponseRedirect(instance.get_absolute_url())
	# else:
	# 	messages.error(request, "Post not Successfully created")

	context = {
		"form": form,
	}
	return render(request, "posts/post_form.html", context)

def post_detail(request, slug=None):
	# instance = Post.objects.get(pk=3)
	instance = get_object_or_404(Post, slug=slug)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:     # if not user cannot create, update or delete post
		    raise Http404
	share_string = quote_plus(instance.content)

	# print(get_read_time(instance.content))
	# print(get_read_time(instance.get_markdown()))

	# comment content_types using generic keys from Comment Model
	# content_type = ContentType.objects.get_for_model(Post)
	# obj_id = instance.id

	# comments = Comment.objects.filter_by_instance(instance)
	# for form data
	initial_data = {         
		"content_type": instance.get_content_type,
		"object_id": instance.id
	}

	form = CommentForm(request.POST or None, initial=initial_data)
	if form.is_valid() and request.user.is_authenticated():
		# print(comment_form.cleaned_data)
		c_type = form.cleaned_data.get("content_type")
		content_type = ContentType.objects.get(model=c_type)
		obj_id = form.cleaned_data.get("object_id")
		content_data = form.cleaned_data.get("content")
		parent_obj = None

		try:			
			parent_id = int(request.POST.get("parent_id"))    # getting parent id for comment to be referenced for reply
		except:
			parent_id = None

		if parent_id:
			parent_qs = Comment.objects.filter(id=parent_id)
			if parent_qs.exists() and parent_qs.count() == 1:
				parent_obj = parent_qs.first()      #if parent comment id exists in database

		new_comment, created = Comment.objects.get_or_create (
									user = request.user,
									content_type = content_type,
									object_id = obj_id,
									content = content_data,
									parent = parent_obj
			                  )

		return HttpResponseRedirect(new_comment.content_object.get_absolute_url())    # redirecting back to comment object

	comments = instance.comments      # using the Post comments property

	context = {
		"instance": instance,
		"share_string": share_string,
		"comments": comments,
		"comment_form": form,
	}
	return render(request, "posts/post_detail.html", context)

def post_update(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:     # if not user cannot create, update or delete post
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=instance)
	if form.is_valid(): 
		instance = form.save(commit=False)
		print(form.cleaned_data.get("title"))
		instance = form.save()
		messages.success(request, "Post Successfully updated")
		return HttpResponseRedirect(instance.get_absolute_url())
	# else:
	# 	messages.error(request, "Post failed to update")

	context = {
		"instance": instance,
		"form": form
	}
	return render(request, "posts/post_editform.html", context)

def post_delete(request, slug=None):
	if not request.user.is_staff or not request.user.is_superuser:     # if not user cannot create, update or delete post
		raise Http404
	instance = get_object_or_404(Post, slug=slug)
	instance.delete()
	messages.success(request, "Post Successfully deleted")
	return redirect("posts:list")
