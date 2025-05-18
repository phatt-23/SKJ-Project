from asyncio import wait
from datetime import datetime, timezone
from django.contrib.auth import get_user_model
from django.contrib.auth.views import login_required
from django.contrib import messages
from django.db.models import Q, Max
from django.db.models.base import Coalesce
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import trim_whitespace

from common.models import Comment, Issue, Repository
from web.utils import SearchParams


def repo_issue_list(request, username, repo_name):
    owner = get_object_or_404(get_user_model(), username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    query = request.GET.get('q')

    filters = Q(repository__owner=owner, repository=repo)
    if query:
        filters &= Q(title__icontains=query) | Q(description__icontains=query)

    if 'status' in request.GET:
        status = request.GET['status']
        if status in ('open', 'closed'):
            filters &= Q(status=status)

    params = SearchParams.from_request(
        request, 
        max_count=100,
        allowed_order_by_columns=['created_at', 'last_active'],
        default_order_by='last_active',
    )

    issues = Issue.objects.annotate(
        last_active=Coalesce(Max('comments__created_at'), 'created_at')
    ).filter(filters)

    issues = params.apply(issues)

    return render(request, 'web/repo_issue_list.html', {
        'owner': owner,
        'repo': repo,
        'issues': issues,
        'query': query or ''
    })

@login_required
def repo_issue_create(request, username, repo_name):
    owner = get_object_or_404(get_user_model(), username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    author = request.user

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')

        if trim_whitespace(title) == '':
            messages.error(request, 'Title is required.')
        if trim_whitespace(description) == '':
            messages.error(request, 'Description is required. Please describe the issue thoroughly.')

        if len(messages.get_messages(request)) == 0:
            issue = Issue.objects.create(title=title, description=description, repository=repo, created_by=author)
            issue.save()
            return redirect('repo_issue_detail', username=owner.username, repo_name=repo.name, issue_id=issue.id)

    return render(request, 'web/repo_issue_create.html', {
        'owner': owner,
        'repo': repo,
    })

def repo_issue_detail(request, username, repo_name, issue_id):
    owner = get_object_or_404(get_user_model(), username=username)
    repo = get_object_or_404(Repository, owner=owner, name=repo_name)
    issue = get_object_or_404(Issue, id=issue_id)
    comments = Comment.objects.filter(issue=issue).order_by('-created_at')

    if request.method == 'POST':
        action = request.POST.get('action')
        content = request.POST.get('content').strip()
        author = request.user

        if action == 'comment':
            if content:
                Comment.objects.create(issue=issue, content=content, author=author)
            else:
                messages.error(request, 'Comment content is required.')
        elif action == 'close':
            if content:
                comment = Comment.objects.create(issue=issue, content=content, author=author)
                issue.closing_comment = comment
            if issue.status == 'open':
                issue.status = 'closed'
                issue.closed_at = datetime.now(timezone.utc)
                issue.save()

    return render(request, 'web/repo_issue_detail.html', {
        'owner': owner,
        'repo': repo,
        'author': issue.created_by,
        'issue': issue,
        'comments': comments,
    })


