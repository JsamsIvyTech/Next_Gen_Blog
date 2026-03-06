from django.urls import path
from .views import (
    BlogListView, 
    BlogDetailView, 
    BlogCreateView, 
    BlogUpdateView, 
    BlogDeleteView, 
    LikeView, 
    ProfileView,
    ProfileUpdateView,
    SignUpView,
    CategoryView,
    TagView,
    LegacyRedirectView
)

urlpatterns = [
    path('', BlogListView.as_view(), name='home'),
    path('post/new/', BlogCreateView.as_view(), name='post-new'),
    path('post/<int:pk>/', LegacyRedirectView, name='post-legacy-redirect'),
    path('post/<slug:slug>/', BlogDetailView.as_view(), name='post-detail'),
    path('post/<slug:slug>/edit/', BlogUpdateView.as_view(), name='post-edit'),
    path('post/<slug:slug>/delete/', BlogDeleteView.as_view(), name='post-delete'),
    path('like/<slug:slug>/', LikeView, name='like-post'),
    path('profile/edit/', ProfileUpdateView.as_view(), name='profile-edit'),
    path('profile/<str:username>/', ProfileView, name='profile'),
    path('category/<str:foo>/', CategoryView, name='category'),
    path('tag/<str:tag>/', TagView, name='tag'),
    path('signup/', SignUpView.as_view(), name='signup'),
]
