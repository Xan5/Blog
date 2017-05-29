from django.db import models
from precise_bbcode.fields import BBCodeTextField
# Create your models here.

from datetime import date
from django.urls import reverse  # Used to generate URLs by reversing the URL patterns
from django.contrib.auth.models import User, Group  # Blog author or commenter


class Blog(models.Model):
    name = models.CharField(max_length=200)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    description = models.TextField(max_length=2000)
    pub_date = models.DateField(default=date.today)
    class Meta:
        ordering = ["pub_date"]

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=200)
    blog = models.ForeignKey(Blog, on_delete=models.SET_NULL, null=True)
    group = models.ForeignKey(Group, default=None, null=True, blank=True)
    content = BBCodeTextField()
    pub_date = models.DateField(default=date.today)
    class Meta:
        ordering = ["pub_date"]

    def get_absolute_url(self):
        return reverse('post-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

    objects = Blog()


class PostComment(models.Model):
    pub_date = models.DateTimeField(auto_now_add=True)
    content = BBCodeTextField(null=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ["pub_date"]

    def __str__(self):

        len_title = 75
        if len(self.description) > len_title:
            titlestring = self.description[:len_title] + '...'
        else:
            titlestring = self.description
        return titlestring

