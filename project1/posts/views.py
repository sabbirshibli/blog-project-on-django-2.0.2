from urllib.parse import quote_plus
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.utils import timezone

from .models import Post
from .forms import PostForm

# Create your views here.

# Create
def post_create(request):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.user = request.user
		instance.save()
		messages.success(request, "Post successfully created!!")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"form": form,
	}
	return render(request, "post_form.html", context)

#Retrive1
def post_detail(request, id='none'):
	instance = get_object_or_404(Post, id=id)
	if instance.draft or instance.publish > timezone.now().date():
		if not request.user.is_staff or not request.user.is_superuser:
			raise Http404
	share_string = quote_plus(instance.content)
	context = {
	    "title": "Details",
		"obj": instance,
		"share_string": share_string
	}
	return render(request, "post_detail.html", context)

#Retrive2
def post_list(request):
	today = timezone.now().date()
	queryset_list = Post.objects.active() #.order_by("-timestamp")
	if request.user.is_staff or request.user.is_superuser:
		queryset_list = Post.objects.all()
	query = request.GET.get("q")
	if query:
		queryset_list = queryset_list.filter(title__icontains=query)
	paginator = Paginator(queryset_list, 5) # Show 25 contacts per page
	page_request_var = "page"
	page = request.GET.get(page_request_var)
	queryset = paginator.get_page(page)
	context = {
		"title": "List",
		"object_list": queryset,
		"page_request_var": page_request_var,
		"today": today,
	}
	return render(request, "post_list.html", context)

#Update
def post_update(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	form = PostForm(request.POST or None, request.FILES or None, instance = instance)
	if form.is_valid():
		instance = form.save(commit=False)
		instance.save()
		messages.success(request, "Post successfully updated!!")
		return HttpResponseRedirect(instance.get_absolute_url())

	context = {
		"title": "Details",
		"obj": instance,
		"form": form,
	}
	return render(request, "post_form.html", context)

#Delete
def post_delete(request, id=None):
	if not request.user.is_staff or not request.user.is_superuser:
		raise Http404
	instance = get_object_or_404(Post, id=id)
	instance.delete()
	messages.success(request, "Post successfully Removed!!")
	return redirect("posts:list")
