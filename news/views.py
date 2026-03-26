from django.shortcuts import redirect, get_object_or_404
from django.views import View
from .models import Category
from .models import Post
import django.core.paginator
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import UpdateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache


@method_decorator(cache_page(60 * 5), name='dispatch')
class NewsListView(ListView):
    model = Post
    template_name = 'news/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    ordering = ['-created_at']

    def get_queryset(self):
        return Post.objects.all()
    

@method_decorator(cache_page(60 * 5), name='dispatch')
class ArticleListView(ListView):
    model = Post
    template_name = 'news/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(type='AR').order_by('-created_at',)


class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


class ArticleDetailView(DetailView):
    model = Post
    template_name = 'news/post_detail.html'
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'post-{self.kwargs["pk"]}', None)

        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'post-{self.kwargs["pk"]}', obj)

        return obj


@method_decorator(cache_page(60 * 5), name='dispatch')
class NewsSearchView(ListView):
    model = Post
    template_name = 'news/post_search.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        qs = Post.objects.all().order_by('-created_at')

        title = self.request.GET.get('title')
        author = self.request.GET.get('author')
        date_from = self.request.GET.get('date_from')

        if title:
            qs = qs.filter(title_icontains=title)

        if author:
            qs = qs.filter(author_username_icontains=author)

        if date_from:
            qs = qs.filter(created_at_gte=date_from)

        return qs
    

class NewsCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.add_post'

    def form_valid(self, form):
        today = timezone.now().date()

        news_today = Post.objects.filter(
            author=self.request.user,
            type='NW',
            created_at__date=today
        ).count()

        if news_today >=3:
            form.add_error(
                None,
                'Вы не можете публиковать более 3 новостей в сутки.'
            )
            return self.form_invalid(form)
        
    
        post = form.save(commit=False)
        post.type = 'NW'
        post.author = self.request.user
        return super().form_valid(form)
    

class NewsUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'news/post_form.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.change_post'

    login_url = '/accounts/login/'

    def get_queryset(self):
        return Post.objects.all()
    

class NewsDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    permission_required = 'news.delete_post'

    def get_queryset(self):
        return Post.objects.filter(type='NW')
    

class ArticleCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Post
    template_name = 'news/post_form.html'
    form_class = PostForm
    permission_required = 'news.add_post'

    def get_success_url(self):
        return reverse_lazy('article_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = 'AR'
        post.author = self.request.user
        return super().form_valid(form)


class ArticleUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Post
    template_name = 'news/post_form.html'
    form_class = PostForm
    permission_required = 'news.change_post'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        return Post.objects.all()


class ArticleDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'news/post_confirm_delete.html'
    success_url = reverse_lazy('article_list')
    permission_required = 'news.delete_post'

    def get_queryset(self):
        return Post.objects.filter(type='AR')


@login_required
def become_author(request):
    author_group = Group.objects.get(name='authors')
    request.user.groups.add(author_group)
    return redirect('/news/')
    

@cache_page(60)
class SubscribeCategoryView(LoginRequiredMixin, View):
    def post(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.subscribers.add(request.user)
        return redirect('category_posts', pk=pk)
    

@method_decorator(cache_page(60 * 5), name='dispatch')
class CategoryPostListView(ListView):
    model = Post
    template_name = 'news/category_posts.html'
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return Post.objects.filter(categories=self.category)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context

