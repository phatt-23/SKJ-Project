from django.db.models import Q
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth import get_user_model

from common.models import Repository


def index(request):
    if request.user.is_authenticated:
        return dashboard(request)
    return render(request, 'web/index.html')


def dashboard(request):
    return render(request, 'web/dashboard.html')


def search_view(request: HttpRequest):
    query = request.GET.get('q')
    users = repos = []
    
    if query:
        users = get_user_model().objects.filter(username__icontains=query)
        repos = Repository.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'web/search_results.html', {
        'query': query,
        'users': users,
        'repos': repos,
    })

