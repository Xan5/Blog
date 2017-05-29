import datetime

from haystack import indexes

from blog.models import Blog, Post, PostComment


class BlogIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    author = indexes.CharField(model_attr='author')
    description = indexes.CharField(model_attr='description')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Blog

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())

class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name')
    blog = indexes.CharField(model_attr='blog')
    content = indexes.CharField(model_attr='content')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())

class PostCommentIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user')
    content = indexes.CharField(model_attr='content')
    pub_date = indexes.DateTimeField(model_attr='pub_date')

    def get_model(self):
        return PostComment

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(pub_date__lte=datetime.datetime.now())
