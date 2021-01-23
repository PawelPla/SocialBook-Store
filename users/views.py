from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import DetailView, ListView, UpdateView


from users.forms import UpdateUserForm


class UserDetail(LoginRequiredMixin, DetailView):
    model = get_user_model()
    template_name = 'profile/profile_detail.html'
    context_object_name = 'profile'


class AllUsers(ListView):
    model = get_user_model()
    template_name = 'profile/profile_list.html'
    context_object_name = 'profiles'
    paginate_by = 5
    ordering = ['username']


class TopReviewers(ListView):
    model = get_user_model()
    template_name = 'profile/top_reviewers.html'
    context_object_name = 'top_reviewers'
    paginate_by = 5

    def get_queryset(self):
        queryset = get_user_model().objects.all().annotate(num_reviews=Count('reviews')).order_by('-num_reviews',
                                                                                                  'username')
        return queryset


class UserUpdate(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    form_class = UpdateUserForm
    template_name = 'profile/profile_update.html'
    success_url = reverse_lazy('blog_home')
    context_object_name = 'updated_user'

    def get_object(self, queryset=None):
        return self.request.user

    def test_func(self):
        if self.request.user == self.get_object():
            return True
        return False


class UserReviews(ListView):
    model = get_user_model()
    template_name = 'profile/profile_reviews.html'
    context_object_name = 'reviewer'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(get_user_model(), pk=self.kwargs.get('pk'))

        return get_user_model().objects.filter(username=user).first().reviews.all()
