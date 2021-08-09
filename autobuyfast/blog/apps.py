from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class BlogConfig(AppConfig):
    name = 'autobuyfast.blog'
    verbose_name = _("Blog")

    def ready(self):
        # story_model = apps.get_model("etopoenergy.blog", "etopoenergy.blog.models.Post")
        # secretballot.enable_voting_on(story_model)
        try:
            import autobuyfast.blog.signals  # noqa F401
        except ImportError:
            pass
