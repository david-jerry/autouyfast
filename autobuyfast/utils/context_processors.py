from category.models import Category, Tag
from django.conf import settings

from autobuyfast.blog.models import Category, Post
from autobuyfast.cars.models import AutoSearch
from autobuyfast.users.models import Testimonial


def settings_context(_request):
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    context = {
        "DEBUG": settings.DEBUG,
        "all_cars": AutoSearch.objects.all()[:10],
        "all_testimony": Testimonial.objects.all().filter(active=True).order_by("-created")[:15],
        "all_reviews": Post.objects.all().filter(tags__title="reviews").order_by("-created")[:10]
    }
    return context

