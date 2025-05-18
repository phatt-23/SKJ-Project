from datetime import datetime, timezone
from django import template
from django.conf import settings
from django.templatetags.static import static

register = template.Library()

@register.filter
def timestamp_iso_format(value, fmt=None):
    if fmt is None:
        fmt = settings.TIMESTAMP_URL_FORMAT
    return value.strftime(fmt)


@register.filter
def language_by_ext(value):
    filepath = str(value)
    ext = filepath.split('.')[-1]

    if ext == 'py':
        return 'python'
    elif ext in ('c', 'cpp'):
        return ext
    elif ext in ('h', 'hpp'):
        return ext

    return 'plaintext'


@register.filter
def last_updated_fmt(date: datetime):
    now = datetime.now(timezone.utc)
    delta = now - date
    seconds = delta.total_seconds()  # don't use delta.seconds !!!

    if seconds < 60:
        return f'{int(seconds)} seconds ago'
    elif seconds < 3600:
        return f'{int(seconds // 60)} minutes ago'
    elif seconds < 86400:
        hours = int(seconds // 3600)
        return 'an hour ago' if hours == 1 else f'{hours} hours ago'
    elif delta.days < 7:
        return 'a day ago' if delta.days == 1 else f'{delta.days} days ago'
    elif delta.days < 30:
        weeks = delta.days // 7
        return 'a week ago' if weeks == 1 else f'{weeks} weeks ago'
    elif delta.days < 365:
        return f'on {date.strftime("%b %d, %Y")}'
    else:
        return f'on {date.strftime("%b %d, %Y")}'

@register.filter
def avatar_url(user):
    try:
        return user.avatar.url
    except:
        return static('defaults/avatar.jpg')


