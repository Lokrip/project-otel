from django.views.generic import View
from django.http import HttpResponse
from django.shortcuts import render

class ViewsBlog(View):
    def get(self, request):
        return render(request, 'config/index.html')
