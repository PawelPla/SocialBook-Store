from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .forms import NewCommentForm
from .models import Post, Comment
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


class HomePageView(ListView):
    model = Post
    ordering = ['-date_posted']
    paginate_by = 5
    context_object_name = 'posts'
    template_name = 'home.html'


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'
    paginate_by = 2
    context_object_name = 'posts'

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            data['comment_form'] = NewCommentForm(instance=self.request.user)

        return data

    def post(self, request, *args, **kwargs):
        new_comment = Comment(
            to_post=self.get_object(),
            content=request.POST.get('content'),
            author=self.request.user
        )
        new_comment.save()
        return self.get(self, request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_create.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content']
    template_name = 'blog/post_update.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('blog_home')
    template_name = 'blog/post_delete_confirm.html'
    context_object_name = 'post'

    def test_func(self):
        if self.request.user == self.get_object().author:
            return True
        return False



