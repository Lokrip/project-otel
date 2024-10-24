from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.ViewsBlog.as_view(), name='blog-page'),
    path('news/<slug:catygory_slug>/', views.CatygoryViewsBlog.as_view(), name='catygory-views-blog'),
    path('tags/<slug:tag_slug>/', views.TagsViewsBlog.as_view(), name='tag_slug'),
    path('detail-views/<slug:blog_slug>/', views.DetailViewBlog.as_view(), name='detail-view-blog'),
    path('detail-views/<slug:blog_slug>/add-message/', views.AddComment.as_view(), name='add-comment')
]


