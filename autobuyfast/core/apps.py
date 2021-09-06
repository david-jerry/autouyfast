from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CoreConfig(AppConfig):
    name = 'autobuyfast.core'
    verbose_name = _("Core")

    def ready(self):
        # story_model = apps.get_model("etopoenergy.blog", "etopoenergy.blog.models.Post")
        # secretballot.enable_voting_on(story_model)
        try:
            import autobuyfast.core.signals  # noqa F401
        except ImportError:
            pass
