from __future__ import absolute_import

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from filebrowser.sites import site

from autobuyfast.cars.views import home
from autobuyfast.users.views import buyer_signup, car_request_view, seller_signup
from config.sitemaps import StaticViewSitemap

sitemaps = {
    "static": StaticViewSitemap,
}

urlpatterns = [
    path("", view=home, name="home"),
    path(
        "about/", view=car_request_view, name="about"
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [
    # Django Admin, use {% url 'admin:index' %}
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("jet/", include("jet.urls", namespace="jet")),
    path("jet/dashboard/", include("jet.dashboard.urls", namespace="jet-dashboard")),
    path("flatpage/", include("django.contrib.flatpages.urls")),
    path(settings.ADMIN_FILEBROWSER_URL, site.urls),
    path(settings.ADMIN_URL, admin.site.urls),
    path(settings.ADMIN_DOC_URL, include("django.contrib.admindocs.urls")),
]

urlpatterns += [
    # Custom users registration
    path("accounts/signup/", buyer_signup, name="account_signup"),
    path("accounts/signup-dealer/", seller_signup, name="seller_signup"),
    path("signup/", TemplateView.as_view(template_name="account/signup.html"), name="signup_select"),

    # User management
    path("users/", include("autobuyfast.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),

    # Your stuff: custom urls includes go here
    path("cars/", include("autobuyfast.cars.urls", namespace="cars")),
]

urlpatterns += [
    path("blog/", include("autobuyfast.blog.urls", namespace="blogs")),
    path('comment/', include('comment.urls')),
]

# SEO url settings
urlpatterns += [
    # SEO stuff: custom urls includes go here
    path("sitemap.xml/", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path(
        "robots.txt/",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain"),
        name="robots",
    ),
    path("tinymce/", include("tinymce.urls")),

    # Language switcher support urls for django
    path("i18n/", include("django.conf.urls.i18n")),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
