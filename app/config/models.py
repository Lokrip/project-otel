from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from mptt.models import MPTTModel, TreeForeignKey


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    image_user = models.ImageField(upload_to='user-image/%Y/%m/%d/', verbose_name='Изоброжение', blank=True, null=True)
    bio = models.TextField(max_length=5000, blank=True, null=True)
    slug = models.SlugField(unique=True, db_index=True)
    
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
    
class CatygoryBlog(MPTTModel):
    name = models.CharField(max_length=120)
    image = models.ImageField(upload_to='cat-image/%Y/%m/%d/', blank=True, null=True)
    parent = TreeForeignKey('self', related_name='children', on_delete=models.SET_NULL, null=True, blank=True)
    slug = models.SlugField(unique=True, db_index=True)

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse("blog:catygory-views-blog", kwargs={"catygory_slug": self.slug})
    
    
    @property
    def counterItem(self):
        blog = Blog.objects.filter(catygory__slug=self.slug).count()
        return blog

    class MPTTMeta:
        order_insertion_by = ['name']
    
    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категорий'
        
class TagsBlog(models.Model):
    name = models.CharField(max_length=120)
    slug = models.SlugField(unique=True, db_index=True)
    
    def get_absolute_url(self):
        return reverse("blog:tag_slug", kwargs={"tag_slug": self.slug})

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        
class Blog(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль')
    name = models.CharField(max_length=120, verbose_name='Имя', db_index=True)
    image = models.ImageField(upload_to='blog-image/%Y/%m/%d/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    catygory = models.ForeignKey(CatygoryBlog, on_delete=models.SET_NULL, null=True)
    tag = models.ManyToManyField(TagsBlog, related_name='post')
    likes = models.PositiveBigIntegerField(default=0)
    draft = models.BooleanField(default=False, verbose_name='Черновик')
    slug = models.SlugField(unique=True, db_index=True)
    update_at = models.DateTimeField(auto_now=True)
    create_at = models.DateTimeField(auto_now_add=True)
    
    
    def __str__(self):
        return f'{self.name}-{self.catygory.name}'
    
    def get_absolute_url(self):
        return reverse('blog:detail-view-blog', kwargs={'blog_slug': self.slug})
    
    @property
    def counterMessage(self):
        message = MessageBlog.objects.filter(blog__slug=self.slug).count()
        return f'{message:02}'  
    
    @property
    def objectMessage(self):
        return MessageBlog.objects.filter(blog__slug=self.slug)
    
    @property
    def tagsPost(self):
        tags = self.tag.all()
        return tags[:5]
    
    class Meta:
        verbose_name = 'Блог'
        verbose_name_plural = 'Блоги'
        
class MessageBlog(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, verbose_name='Профиль')
    name = models.CharField(max_length=120, verbose_name='Имя', db_index=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='блог')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, verbose_name='ответ', blank=True, null=True)
    slug = models.SlugField(unique=True, db_index=True)
    update_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return f'Сообщение {self.name} для {self.blog.name}'
    
    
    class Meta:
        verbose_name = 'Сообщение для блога'
        verbose_name_plural = 'Сообщение для блога'
        
        
# class CatygoryNews(models.Model): 
#     name = models.CharField(max_length=120)
#     slug = models.SlugField(unique=True, db_index=True)
    
#     def __str__(self):
#         return self.name
    
#     class Meta:
#         verbose_name = 'Категория для Новостей'
#         verbose_name__plural = 'Категорий для Новостей'
        
# class TagsNews(models.Model):
#     name = models.CharField(max_length=120)
#     slug = models.SlugField(unique=True, db_index=True)
    
#     def __str__(self):
#         return self.name
    
#     class Meta:
#         verbose_name = 'Теги для Новостей'
#         verbose_name__plural = 'Теги для Новостей'
        
        
# class YouTubeVideo(models.Model):
#     title = models.CharField(max_length=200)
#     catygory = models.ForeignKey(CatygoryNews, on_delete=models.SET_NULL, null=True)
#     video_id = models.CharField(max_length=120, unique=True)
#     description = models.TextField(blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     slug = models.SlugField(unique=True, db_index=True)

#     def __str__(self):
#         return self.title
    
#     def get_embed_url(self):
#         return f"https://www.youtube.com/embed/{self.video_id}"
    
#     class Meta:
#         verbose_name = 'Видео с YouTube'
#         verbose_name_plural = 'Видео с YouTube'