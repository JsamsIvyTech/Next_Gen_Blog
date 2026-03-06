from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Category, Comment, Profile, Tag
from .forms import CommentForm, ProfileForm, PostForm
from django.urls import reverse_lazy, reverse
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Welcome {form.cleaned_data.get('username')}! Your account has been created.")
        return response

def LikeView(request, slug):
    if not request.user.is_authenticated:
        messages.warning(request, "Please login to like posts.")
        return redirect('login')
    post = get_object_or_404(Post, slug=slug)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        messages.info(request, "Post unliked.")
    else:
        post.likes.add(request.user)
        messages.success(request, "Post liked!")
    return HttpResponseRedirect(reverse('post-detail', args=[str(slug)]))

class BlogListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-created_at']
    paginate_by = 6

    def get_queryset(self):
        query = self.request.GET.get('q')
        queryset = Post.objects.filter(status='published')
        if query:
            queryset = queryset.filter(Q(title__icontains=query) | Q(body__icontains=query)).distinct()
        return queryset

class BlogDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        context["total_likes"] = post.total_likes()
        context["liked"] = liked
        context["comment_form"] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Your comment has been posted!")
            return redirect('post-detail', slug=post.slug)
        return self.get(request, *args, **kwargs)

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_new.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)

class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_edit.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_delete.html'
    success_url = reverse_lazy('home')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
    
    def delete(self, request, *args, **kwargs):
        messages.warning(self.request, "Post deleted.")
        return super().delete(request, *args, **kwargs)

def ProfileView(request, username):
    profile = get_object_or_404(Profile, user__username=username)
    posts = Post.objects.filter(author=profile.user, status='published').order_by('-created_at')
    return render(request, 'blog/profile.html', {'profile': profile, 'posts': posts})

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileForm
    template_name = 'blog/profile_edit.html'
    
    def get_object(self):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile

    def get_success_url(self):
        messages.success(self.request, "Profile updated.")
        return reverse('profile', kwargs={'username': self.request.user.username})

def CategoryView(request, foo):
    category_posts = Post.objects.filter(category__name__iexact=foo.replace('-', ' '), status='published')
    return render(request, 'blog/category.html', {'foo': foo.title().replace('-', ' '), 'category_posts': category_posts})

def TagView(request, tag):
    tag_posts = Post.objects.filter(tags__name__iexact=tag, status='published')
    return render(request, 'blog/tag.html', {'tag': tag, 'tag_posts': tag_posts})

def LegacyRedirectView(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return redirect('post-detail', slug=post.slug)
