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


