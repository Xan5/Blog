# Create your views here.


import operator


from django.views import generic
from .models import Blog, PostComment, Post
from django.contrib.auth.models import User  # Blog author or commenter
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from blog.forms import SignUpForm
from django.urls import reverse


def index(request):
    """
    View function for home page of site.
    """
    # Render the HTML template index.html
    return render(
        request,
        'index.html',
    )

def redirectSearch(request):
    return render(request,"search/search.html")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

class BlogListView(generic.ListView):
    """
    Generic class-based view for a list of all blogs.
    """
    model = Blog
    paginate_by = 5


class PostListView(generic.ListView):
    model = Post
    paginate_by = 15

class PostCommentListView(generic.ListView):
    model = PostComment
    paginate_by = 15

from django.shortcuts import get_object_or_404


class BlogListbyAuthorView(generic.ListView):
    """
    Generic class-based view for a list of blogs posted by a particular BlogAuthor.
    """
    model = Blog
    paginate_by = 5
    template_name = 'blog/blog_list_by_author.html'

    def get_queryset(self):
        """
        Return list of Blog objects created by BlogAuthor (author id specified in URL)
        """
        author = self.kwargs['author']
        target_author = get_object_or_404(Blog, author=author)
        return Blog.objects.filter(author=target_author)

    def get_context_data(self, **kwargs):
        """
        Add BlogAuthor to context so they can be displayed in the template
        """
        # Call the base implementation first to get a context

        context = super(BlogListbyAuthorView, self).get_context_data(**kwargs)
        # Get the blogger object from the "pk" URL parameter and add it to the context
        context['blogger'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

class BlogDetailView(generic.DetailView):
    """
    Generic class-based detail view for a blog.
    """
    model = Blog
    paginate_by = 15
    template_name = 'blog/blog_detail.html'
    context_object_name = 'post_list'
    def get_context_data(self, **kwargs):
        context = super(BlogDetailView,self).get_context_data(**kwargs)
        id = self.kwargs['pk']
        target = get_object_or_404(Blog, pk=id)
        context['post_list'] = Post.objects.filter(blog = target)
        return context

    def return_blog(self):
        id = self.kwargs['pk']
        blog = get_object_or_404(Blog, pk=id)
        return blog

class PostDetailView(generic.DetailView):
    """
    Generic class-based detail view for a post.
    """
    model = Post
    paginate_by = 15
    template_name = 'blog/post_detail.html'
    context_object_name = 'comment_list'

    def get_context_data(self, **kwargs):
        context = super(PostDetailView,self).get_context_data(**kwargs)
        id = self.kwargs['pk']
        target = get_object_or_404(Post, pk=id)
        context['comment_list'] = PostComment.objects.filter(post = target)
        return context


    def return_post(self):
        id = self.kwargs['pk']
        post = get_object_or_404(Post, pk=id)
        return post


    def dispatch(self, request, *args, **kwargs):
        id = self.kwargs['pk']
        post = get_object_or_404(Post, pk=id)
        if post.group != None:
            if self.request.user.is_superuser or self.request.user.groups.filter(name=post.group).exists():
                return super(PostDetailView, self).dispatch(request, *args, **kwargs)
            else:
                return render(request,'blog/auth_error.html')
        else:
            return super(PostDetailView, self).dispatch(request, *args, **kwargs)

class BloggerListView(generic.ListView):
    """
    Generic class-based view for a list of bloggers.
    """
    # trzeba przefiltrowac listview
    model = Blog
    paginate_by = 5


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import CreateView
from django.urls import reverse


class PostCommentCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a blog comment. Requires login. 
    """
    model = PostComment
    fields = ['content', ]

    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(PostCommentCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        # Add logged-in user as author of comment
        form.instance.author = self.request.user
        # Associate comment with blog based on passed id
        form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(PostCommentCreate, self).form_valid(form)

    def get_success_url(self):
        """
        After posting comment return to associated blog.
        """
        return reverse('post-detail', kwargs={'pk': self.kwargs['pk'], })

class PostCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a blog comment. Requires login.
    """
    model = Post

    fields = ['name','content','group', ]
    def get_context_data(self, **kwargs):
        """
        Add associated blog to form template so can display its title in HTML.
        """
        # Call the base implementation first to get a context
        context = super(PostCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        context['blog'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
        """
        Add author and associated blog to form data before setting it as valid (so it is saved to model)
        """
        # Associate comment with blog based on passed id
        form.instance.blog = get_object_or_404(Blog, pk=self.kwargs['pk'])
        # Call super-class form validation behaviour
        return super(PostCreate, self).form_valid(form)

    def get_success_url(self):
        """
        After posting comment return to associated blog.
        """
        return reverse('blog-detail', kwargs={'pk': self.kwargs['pk'], })

class BlogCreate(LoginRequiredMixin, CreateView):
    """
    Form for adding a blog comment. Requires login.
    """
    model = Blog
    fields = ['name','description', ]

    #def get_context_data(self, **kwargs):

        # Call the base implementation first to get a context
        #context = super(BlogCreate, self).get_context_data(**kwargs)
        # Get the blog from id and add it to the context
        #context['user'] = get_object_or_404(Blog, pk=self.kwargs['pk'])
        #return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(BlogCreate, self).form_valid(form)

    def get_success_url(self):
        return reverse('blogs')
