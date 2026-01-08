from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy, reverse
from .models import Post, Genre, Comment, PostLike, CommentLike, Follow, UserProfile
from .forms import PostForm, CommentForm
import json


class HomePageView(ListView):
    """
    Homepage displaying recent blog posts
    """
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    paginate_by = 6
    
    def get_queryset(self):
        return Post.objects.filter(is_published=True).select_related('author', 'genre').prefetch_related('likes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genres'] = Genre.objects.all()
        context['featured_posts'] = Post.objects.filter(is_published=True)[:3]
        return context


class PostDetailView(DetailView):
    """
    Individual post detail view with comments
    """
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get comments (only parent comments, replies loaded via template)
        comments = Comment.objects.filter(post=post, parent=None).select_related('author').prefetch_related('replies')
        context['comments'] = comments
        context['comment_form'] = CommentForm()
        
        # Check if user has liked the post
        if self.request.user.is_authenticated:
            context['user_has_liked'] = post.is_liked_by(self.request.user)
        
        # Related posts
        context['related_posts'] = Post.objects.filter(
            genre=post.genre,
            is_published=True
        ).exclude(id=post.id)[:3]
        
        return context


class GenrePostsView(ListView):
    """
    Posts filtered by genre
    """
    model = Post
    template_name = 'blog/genre_posts.html'
    context_object_name = 'posts'
    paginate_by = 8
    
    def get_queryset(self):
        self.genre = get_object_or_404(Genre, slug=self.kwargs['slug'])
        return Post.objects.filter(
            genre=self.genre,
            is_published=True
        ).select_related('author', 'genre').prefetch_related('likes')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['genre'] = self.genre
        context['genres'] = Genre.objects.all()
        return context


class CreatePostView(LoginRequiredMixin, CreateView):
    """
    Create new blog post
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Your post has been created successfully!')
        return super().form_valid(form)


class UpdatePostView(LoginRequiredMixin, UpdateView):
    """
    Edit existing blog post
    """
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, 'Your post has been updated successfully!')
        return super().form_valid(form)


class DeletePostView(LoginRequiredMixin, DeleteView):
    """
    Delete blog post
    """
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:home')
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Your post has been deleted.')
        return super().delete(request, *args, **kwargs)


class UserProfileView(DetailView):
    """
    User profile page showing posts and stats
    """
    model = User
    template_name = 'blog/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        context['posts'] = Post.objects.filter(
            author=user,
            is_published=True
        ).select_related('genre').prefetch_related('likes')[:10]
        
        # Check if current user follows this profile user
        if self.request.user.is_authenticated:
            context['is_following'] = Follow.objects.filter(
                follower=self.request.user,
                following=user
            ).exists()
        
        return context


class FollowingFeedView(LoginRequiredMixin, ListView):
    """
    Feed showing posts from followed users
    """
    model = Post
    template_name = 'blog/following_feed.html'
    context_object_name = 'posts'
    paginate_by = 8
    
    def get_queryset(self):
        # Get users that current user follows
        following_users = Follow.objects.filter(
            follower=self.request.user
        ).values_list('following', flat=True)
        
        return Post.objects.filter(
            author__in=following_users,
            is_published=True
        ).select_related('author', 'genre').prefetch_related('likes')


# AJAX Views for likes, comments, follows
@login_required
@require_http_methods(["POST"])
@csrf_exempt
def like_post(request, slug):
    """
    AJAX view to like/unlike posts
    """
    post = get_object_or_404(Post, slug=slug)
    like, created = PostLike.objects.get_or_create(
        user=request.user,
        post=post
    )
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': post.likes_count
    })


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def like_comment(request, comment_id):
    """
    AJAX view to like/unlike comments
    """
    comment = get_object_or_404(Comment, id=comment_id)
    like, created = CommentLike.objects.get_or_create(
        user=request.user,
        comment=comment
    )
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    return JsonResponse({
        'liked': liked,
        'likes_count': comment.likes_count
    })


@login_required
@require_http_methods(["POST"])
def add_comment(request, slug):
    """
    Add comment or reply to post
    """
    post = get_object_or_404(Post, slug=slug)
    parent_id = request.POST.get('parent_id')
    content = request.POST.get('content')
    
    if content:
        parent = None
        if parent_id:
            parent = get_object_or_404(Comment, id=parent_id)
        
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content,
            parent=parent
        )
        
        messages.success(request, 'Comment added successfully!')
    else:
        messages.error(request, 'Comment content cannot be empty.')
    
    return redirect('blog:post_detail', slug=slug)


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def follow_user(request, username):
    """
    AJAX view to follow/unfollow users
    """
    user_to_follow = get_object_or_404(User, username=username)
    
    if user_to_follow == request.user:
        return JsonResponse({
            'error': 'You cannot follow yourself'
        }, status=400)
    
    follow, created = Follow.objects.get_or_create(
        follower=request.user,
        following=user_to_follow
    )
    
    if not created:
        follow.delete()
        following = False
    else:
        following = True
    
    return JsonResponse({
        'following': following,
        'followers_count': user_to_follow.followers.count()
    })


@login_required
@require_http_methods(["POST"])
@csrf_exempt
def toggle_dark_mode(request):
    """
    AJAX view to toggle user's dark mode preference
    """
    try:
        data = json.loads(request.body)
        dark_mode = data.get('dark_mode', False)
        
        profile, created = UserProfile.objects.get_or_create(user=request.user)
        profile.dark_mode = dark_mode
        profile.save()
        
        return JsonResponse({'success': True, 'dark_mode': dark_mode})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})