from django.contrib.auth.views import login_required
from django.db.models import Q, Max
from django.db.models.base import Coalesce
from django.http import HttpRequest
from django.shortcuts import render
from django.contrib.auth import get_user_model

from common.models import Commit, Issue, Repository


def index(request):
    if request.user.is_authenticated:
        return dashboard(request)
    return render(request, 'web/index.html')


@login_required
def dashboard(request):
    me = request.user

    my_repos_open_issues = Issue.objects.filter(
        repository__owner=me, status='open'
    ).annotate(
        last_active=Coalesce(Max('comments__created_at'), 'created_at')
    ).order_by('-last_active')

    my_issues = Issue.objects.filter(
        created_by=me
    ).annotate(
        last_active=Coalesce(Max('comments__created_at'), 'created_at')
    ).order_by('-last_active')

    repos = Repository.objects.filter(owner=me)

    my_recent_commits = Commit.objects.filter(author=me).order_by('-timestamp')

    return render(request, 'web/dashboard.html', {
        'my_repos_open_issues': my_repos_open_issues,
        'repos': repos,
        'my_issues': my_issues,
        'my_open_issues': my_issues.filter(status='open'),
        'my_closed_issues': my_issues.filter(status='closed'),
        'my_recent_commits': my_recent_commits[:10],
    })


def search_view(request: HttpRequest):
    query = str(request.GET.get('q')).strip()
    search = str(request.GET.get('s')).strip()
    users = repos = []
    
    if query:
        if len(search) == 0:
            users = get_user_model().objects.filter(username__icontains=query)
            repos = Repository.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
        if search == 'users':
            users = get_user_model().objects.filter(username__icontains=query)
        if search == 'repos':
            repos = Repository.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))

    return render(request, 'web/search_results.html', {
        'query': query,
        'users': users,
        'repos': repos,
    })

