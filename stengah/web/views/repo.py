import dataclasses
from datetime import UTC, datetime, timedelta, timezone
from django.contrib import messages 
from math import floor
from typing import Optional, List
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Max, OuterRef, QuerySet, Subquery
from django.db.models.base import Coalesce
from django.http.request import BadRequest
from django.shortcuts import redirect, render, get_object_or_404
from django.http import Http404, HttpRequest, JsonResponse
from django.contrib.auth import get_user_model
from common.models import (
    Issue,
    Repository,
    File,
    Commit,
)
from web.utils import SearchParams

def repo_page(request, username, repo_name):
    """
    Repo page with current files.
    Must get the latest commited files. This is done by this query:
        select cf.path
            , cc.message
            , cc.timestamp
        from common_repository cr
        join common_commit cc on cr.id = cc.repository_id
        join common_file cf on cc.id = cf.commit_id
        where cr.id = (select id from common_repository where name = 'repo 2')
        group by cf.path
        having max(cc.timestamp)


    The Djanog query does this, which is equivalent:
        SELECT cf.path, cc.message, cc.timestamp
        FROM common_repository cr
        JOIN common_commit cc ON cr.id = cc.repository_id
        JOIN common_file cf ON cc.id = cf.commit_id
        WHERE cr.name = 'repo 2'
        AND (cf.path, cc.timestamp) IN (
            SELECT cf2.path, MAX(cc2.timestamp)
            FROM common_commit cc2
            JOIN common_file cf2 ON cc2.id = cf2.commit_id
            WHERE cc2.repository_id = cr.id
            GROUP BY cf2.path
        )
    """

    owner = get_object_or_404(get_user_model(), username=username)
    repo = get_object_or_404(Repository, name=repo_name, owner=owner)
    commits = Commit.objects.filter(repository=repo).order_by('-timestamp')
    issues = Issue.objects.annotate(
        last_active_value=Coalesce(Max('comments__created_at'), 'created_at')
    ).filter(repository=repo, status='open').order_by('-last_active_value')

    # for each path, get the latest commit timestamps
    latest_commit_timestamps = File.objects.filter(
        commit__repository=repo,
        path=OuterRef('path')
    ).values('path').annotate(
        latest=Max('commit__timestamp')
    ).values('latest')

    # latest per group
    latest_files = File.objects.filter(
        commit__repository=repo,
        commit__timestamp=Subquery(latest_commit_timestamps)
    )

    return render(request, 'web/repo_page.html', {
        'owner': owner,
        'repo': repo,
        'commits': commits[:10],
        'total_commits': len(commits),
        'files': latest_files,
        'issues': issues[:10],
        'total_issues': len(issues),
        'is_my_page': owner.username == request.user.username,
    })

@login_required
def edit_page(request, username, repo_name):
    if request.user.username != username:
        return Http404('Unauthorized access :(')

    owner = get_object_or_404(get_user_model(), username=username)
    repo = get_object_or_404(Repository, name=repo_name, owner=owner)

    if request.method == 'POST':
        repo.name = request.POST.get('name')
        repo.description = request.POST.get('description')
        repo.is_public = request.POST.get('visibility') == 'public'
        repo.save()
        return redirect('repo_page', username=owner.username, repo_name=repo.name)

    return render(request, 'web/repo_edit_page.html', {
        'owner': owner,
        'repo': repo,
    })


def repo_list(request, username):
    owner = get_object_or_404(get_user_model(), username=username)

    filters = Q(owner=owner)

    if 'q' in request.GET:
        filters &= Q(name__icontains=request.GET['q']) | Q(description__icontains=request.GET['q'])

    params = SearchParams.from_request(
        request, 
        max_count=100,
        allowed_order_by_columns=['created_at', 'name'],
        default_order_by='created_at',
    )

    repos = Repository.objects.filter(filters)
    repos = params.apply(repos)

    is_my_page = username == request.user.username if request.user.is_authenticated else False

    return render(request, 'web/user_repo_list.html', {
        'owner': owner,
        'repos': repos,
        'is_my_page': is_my_page,
    })


@login_required
def repo_create(request):
    owner = get_object_or_404(get_user_model(), username=request.user.username)

    if request.method == 'POST':
        name = request.POST.get('name').strip()
        description = request.POST.get('description')
        is_public = request.POST.get('visibility') == 'public'
        
        if ' ' in name:
            messages.error(request, 'Repository name should not contain any spaces or special characters.')
        
        if len(messages.get_messages(request)) == 0:
            Repository.objects.create(owner=owner, name=name, description=description, is_public=is_public)
            return redirect('user_repo_list', username=owner.username)

    return render(request, 'web/repo_create.html')


@login_required
def repo_delete(request, username, repo_name):
    if request.user.username != username:
        return Http404('Cant edit repostiries of other users.')

    owner = get_object_or_404(get_user_model(), username=username)
    repo = get_object_or_404(Repository, name=repo_name, owner=owner)

    if request.method == 'POST':
        repo.delete()
        return redirect('user_page', username=username)

    return render(request, 'web/repo_delete_page.html', {
        'repo': repo,
        'owner': owner,
    })


