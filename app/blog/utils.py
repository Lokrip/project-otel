from config.models import Blog

class DataMixin:
    def get_blog_search(self, **kwargs):
        return {'blogList': Blog.objects.filter(name__icontains=kwargs.get('query', ''))}