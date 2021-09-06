from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class CareerConfig(AppConfig):
    name = 'autobuyfast.career'
    verbose_name = _("Careers")

    def ready(self):
        # story_model = apps.get_model("etopoenergy.blog", "etopoenergy.blog.models.Post")
        # secretballot.enable_voting_on(story_model)
        try:
            import autobuyfast.career.signals  # noqa F401
        except ImportError:
            pass
