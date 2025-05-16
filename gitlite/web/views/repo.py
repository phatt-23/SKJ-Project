from django.contrib.auth.decorators import login_required
from django.http.request import BadRequest
from django.shortcuts import render, get_object_or_404
from django.http import HttpRequest
from django.contrib.auth import get_user_model
from common.models import (
    Repository,
    File,
    Commit,
)


def repo_page(request, username, repo_name):
    owner = get_object_or_404(get_user_model(), username=username)
    repo = get_object_or_404(Repository, name=repo_name, owner=owner)
    # commits = Commit.objects.filter(repository=repo)
    # files = File.objects.filter(commit=commits)
    
    return render(request, 'web/repo_page.html', {
        'owner': owner,
        'repo': repo,
    })


def repo_list(request, username):
    owner = get_object_or_404(get_user_model(), username=username)
    repos = Repository.objects.filter(owner=owner)

    return render(request, 'web/user_repo_list.html', {
        'owner': owner,
        'repos': repos,
    })


@login_required
def repo_create(request):
    if request.method == 'POST':
        raise BadRequest('not implemented') 

    return render(request, 'web/repo_create.html')


