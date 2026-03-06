from django import forms
from .models import Comment, Profile, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Your Name'}),
            'body': forms.Textarea(attrs={'placeholder': 'Write your comment here...', 'rows': 4}),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'profile_pic', 'website_url', 'twitter_url', 'github_url')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'category', 'tags', 'featured_image', 'status')
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter post title...'}),
            'body': forms.Textarea(attrs={'placeholder': 'Tell your story...', 'rows': 15}),
            'featured_image': forms.URLInput(attrs={'placeholder': 'https://example.com/image.jpg'}),
        }
