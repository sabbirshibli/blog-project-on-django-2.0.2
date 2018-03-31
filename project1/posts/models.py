from django.db import models
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils.text import slugify
from django.conf import settings
from django.utils import timezone

# Create your models here.

class PostManager(models.Manager):
	def active(self, *args, **kwargs):
		# Post.objects.all() = super(PostManager, self).all()
		return super(PostManager, self).filter(draft=False).filter(publish__lte=timezone.now())

def upload_location(obj, filename):
	# filebase, extension = filename.split(".")
	# return "%s/%s.%s" %(obj.id, obj.id, extension)
	return "%s/%s" %(obj.id, filename)

class Post(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.DO_NOTHING)
	title = models.CharField(max_length = 120)
	slug = models.SlugField(unique=True)
	image = models.ImageField(upload_to=upload_location, null=True, blank=True, height_field="height_field", width_field="width_field")
	height_field = models.IntegerField(default=0)
	width_field = models.IntegerField(default=0)
	content = models.TextField(max_length = 500)
	draft = models.BooleanField(default=False)
	publish = models.DateField(auto_now=False, auto_now_add=False)
	# email = models.EmailField(max_length=254)
	updated = models.DateTimeField(auto_now=True, auto_now_add=False)
	timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

	objects = PostManager()

	def __str__(self):
	    return self.title

	def get_absolute_url(self):
		return reverse("posts:detail", kwargs={"id": self.id})

	class Meta:
		ordering = ["-id", "-timestamp", "-updated"]

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
	if not instance.slug:
		instance.slug = create_slug(instance)


pre_save.connect(pre_save_post_receiver, sender=Post)
