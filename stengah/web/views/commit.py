from datetime import UTC, datetime
from typing import Any, List
from django.contrib.auth import get_user_model
from django.contrib.auth.views import login_required
from django.db.models import Q
from django.http import Http404, HttpRequest, JsonResponse
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render

from common.models import Commit, File, Repository
from stengah.settings import TIMESTAMP_URL_FORMAT
from web.utils import SearchParams


def commit_detail(request, username, repo_name, commit_id):
    owner = get_object_or_404(get_user_model(), username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    commit = get_object_or_404(Commit, repository=repo, pk=commit_id)
    files = get_list_or_404(File, commit=commit)

    return render(request, 'web/repo_commit_detail.html', {
        'owner': owner,
        'repo': repo,
        'commit': commit,
        'files': files,
    })


def commit_list(request: HttpRequest, username, repo_name):
    owner = get_object_or_404(get_user_model(), username=username)
    repo = get_object_or_404(Repository, name=repo_name, owner=owner)

    filters = Q(repository=repo)
    query = request.GET.get('q')

    if query:
        filters &= Q(message__icontains=query)

    params = SearchParams.from_request(
        request, 
        max_count=100,
        allowed_order_by_columns=['author', 'timestamp'],
        default_order_by='timestamp',
    )

    commits = Commit.objects.filter(filters)
    commits = params.apply(commits)

    return render(request, 'web/repo_commit_list.html', {
        'repo': repo,
        'commits': commits,
        'owner': owner,
        'query': query or '',
    })


@login_required
def commit_create(request: HttpRequest, username, repo_name):
    owner = get_object_or_404(get_user_model(), username=username)
    repo = get_object_or_404(Repository, name=repo_name, owner=owner)

    if request.method == 'POST':
        uploaded_files = request.FILES.getlist('files')

        if len(uploaded_files) == 0:
            raise Http404('No files were uploaded')

        commit = Commit.objects.create(
            repository=repo,
            message=request.POST.get('message')
        )

        for f in uploaded_files:
            try:
                content = f.read().decode('utf-8')  
            except UnicodeDecodeError:
                content = "[Could not decode file as UTF-8]"

            File.objects.create(
                commit=commit,
                path=f.name,  # is the file itself or relative path to it
                content=content,
            )

        return redirect(
            'repo_commit_detail', 
            username=username, 
            repo_name=repo_name, 
            commit_id=commit.id
        )

    return render(request, 'web/repo_commit_create.html', {
        'owner': owner,
        'repo': repo,
    })


