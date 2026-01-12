from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Main pages
    path('', views.HomePageView.as_view(), name='home'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('genre/<slug:slug>/', views.GenrePostsView.as_view(), name='genre_posts'),
    path('following/', views.FollowingFeedView.as_view(), name='following_feed'),

    # Post CRUD
    path('create/', views.CreatePostView.as_view(), name='create_post'),
    path('post/<slug:slug>/edit/', views.UpdatePostView.as_view(), name='edit_post'),
    path('post/<slug:slug>/delete/', views.DeletePostView.as_view(), name='delete_post'),

    # User profiles
    path('user/<str:username>/', views.UserProfileView.as_view(), name='user_profile'),

    # AJAX endpoints
    path('ajax/like-post/<slug:slug>/', views.like_post, name='like_post'),
    path('ajax/like-comment/<int:comment_id>/', views.like_comment, name='like_comment'),
    path('ajax/follow/<str:username>/', views.follow_user, name='follow_user'),
    path('ajax/toggle-dark-mode/', views.toggle_dark_mode, name='toggle_dark_mode'),

    # Comments
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
]