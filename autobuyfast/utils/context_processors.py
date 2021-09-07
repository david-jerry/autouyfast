from category.models import Category, Tag
from django.conf import settings

from autobuyfast.blog.models import Category, Post
from autobuyfast.cars.models import AutoSearch
from autobuyfast.core.models import EmailSubscribe, Faq
from autobuyfast.users.models import Testimonial, User


def settings_context(_request):
    """Settings available by default to the templates context."""
    # Note: we intentionally do NOT expose the entire settings
    # to prevent accidental leaking of sensitive information
    # cat_rev = Category.objects.get(slug="reviews")
    # cat_news = Category.objects.get(slug="news")
    context = {
        "DEBUG": settings.DEBUG,
        "latest_news": Post.objects.all_posts().filter(categories__slug="news").order_by("-pub_date")[:3],
        "latest_reviews": Post.objects.all_posts().filter(categories__slug="reviews").order_by("-pub_date")[:3],
        "all_dealers": User.objects.filter(is_seller=True),
        "featured_dealers": User.objects.filter(featured=True, is_seller=True)[:20],
        "all_cars": AutoSearch.objects.all_cars()[:10],
        "all_faqs": Faq.objects.all_faq(),
        "dealers_count": User.objects.filter(is_seller=True).count(),
        "car_count": AutoSearch.objects.all_cars().filter(available=True).count(),
        "all_featured_cars": AutoSearch.objects.featured_cars()[:5],
        "all_special_cars": AutoSearch.objects.special_offers()[:5],
        "all_testimony": Testimonial.objects.all().filter(active=True).order_by("-created")[:15],
        "all_reviews": Post.objects.all_posts().filter(categories__slug="reviews").order_by("-pub_date")[:10],
        "two_reviews": Post.objects.all_posts().filter(categories__slug="reviews").order_by("-pub_date")[:2],
        "three_reviews": Post.objects.all_posts().filter(categories__slug="reviews").order_by("-pub_date")[1:4],
        "all_posts": Post.objects.all_posts().filter(categories__slug="news").order_by("-pub_date")[:10],
        "all_faq": Faq.objects.all_faq()[:10]
    }
    return context

