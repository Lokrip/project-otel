from typing import Any
from django.db.models.query import QuerySet
from django.core.paginator import Paginator
from django.views.generic import View, ListView, DetailView
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from blog.utils import DataMixin
from django.db import connection

from config.models import *
from .forms import MessageForm

class ViewsBlog(DataMixin, ListView):
    model = Blog
    template_name = 'blog/blog.html'
    context_object_name = 'blogList'
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context.update(self.get_blog_search(query=self.request.GET.get('q', '')))
        blog_list  = context['blogList']
        paginator = Paginator(blog_list, 1) #Расделяем элемент так чтобы на кадой страници погинация было по 1 элементы
        
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)
        
        context['blogList'] = page_obj
        context['title'] = 'Блоги Сайта'
        context['page_obj'] = page_obj
        
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return Blog.objects.filter(draft=False)
    
class DetailViewBlog(DetailView):
    model = Blog
    template_name = 'blog/detail-views/single-blog.html'
    context_object_name = 'blogItem'
    slug_field = 'slug' #C чем будем сравнивать полученный слаг тоесть сравниваем в модели с полям slug
    slug_url_kwarg = 'blog_slug' #Тоесть мы его будем сравнивать с
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        blogItem = self.object
        context['title'] = 'Статья -' + blogItem.name[:5] + '...'
        context['form'] = MessageForm()
        return context
    
class AddComment(View):
    def post(self, request, blog_slug):
        form = MessageForm(request.POST)
        if form.is_valid():
            time_save = form.save(commit=False)
            time_save.blog = Blog.objects.get(slug=blog_slug)
            time_save.profile = request.user.profile
            time_save.save()
            return redirect('blog:detail-view-blog', blog_slug)
        return redirect('blog:detail-view-blog', blog_slug)
    
    
class CatygoryViewsBlog(ListView):
    model = CatygoryBlog
    template_name = 'blog/blog.html'
    context_object_name = 'blogList'   
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        CatygoryItem = CatygoryBlog.objects.get(slug=self.kwargs.get('catygory_slug'))
        context['title'] = 'Блоги про - ' + CatygoryItem.name
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return Blog.objects.filter(catygory__slug=self.kwargs.get('catygory_slug'))


class TagsViewsBlog(ListView):
    model = TagsBlog
    template_name = 'blog/blog.html'
    context_object_name = 'blogList'
    
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        TagItem = TagsBlog.objects.get(slug=self.kwargs.get('tag_slug'))
        context['title'] = 'Блоги про - ' + TagItem.name
        return context

    def get_queryset(self) -> QuerySet[Any]:
        return Blog.objects.filter(tag__slug=self.kwargs.get('tag_slug'))