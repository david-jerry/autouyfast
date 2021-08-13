from django.conf import settings

from autobuyfast.blog.models import Category, Post
from autobuyfast.cars.models import AutoSearch


def settings_context(_request):
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    context = {
        "DEBUG": settings.DEBUG,
        "all_cars": AutoSearch.objects.all()[:10]
    }
    return context

