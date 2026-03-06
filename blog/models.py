from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def __str__(self):
        return self.name

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    featured_image = models.URLField(max_length=500, blank=True, null=True, help_text="Paste a URL to a cover image")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    likes = models.ManyToManyField(User, related_name='blog_posts', blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            original_slug = slugify(self.title)
            slug = original_slug
            counter = 1
            while Post.objects.filter(slug=slug).exists():
                slug = f"{original_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'slug': self.slug})

    @property
    def reading_time(self):
        word_count = len(self.body.split())
        return max(1, round(word_count / 200))

    def total_likes(self):
        return self.likes.count()

class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.name)

class Profile(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True)
    profile_pic = models.URLField(max_length=500, blank=True, null=True)
    website_url = models.URLField(max_length=200, null=True, blank=True)
    twitter_url = models.URLField(max_length=200, null=True, blank=True)
    github_url = models.URLField(max_length=200, null=True, blank=True)

    def __str__(self):
        return str(self.user)

