from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from django.contrib.auth.views import (
    LoginView, LogoutView, PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView,
)

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from apps.search import views as search_views
from apps.home import views as home_views

urlpatterns = [
    # Django
    path("login/",
         LoginView.as_view(
             template_name="login.html",
             redirect_authenticated_user=True
         ),
         name="login"),
    path('logout/', LogoutView.as_view(), name='logout'),

    path("password-change/",
         PasswordChangeView.as_view(),
         name="password_change"),
    path("password-change/done/",
         PasswordChangeDoneView.as_view(),
         name="password_change_done"),

    path("password-reset/",
         PasswordResetView.as_view(),
         name="password_reset"),
    path("password-reset/done/",
         PasswordResetDoneView.as_view(),
         name="password_reset_done"),
    path("password-reset/confirm/<uidb64>/<token>/",
         PasswordResetConfirmView.as_view(),
         name="password_reset_confirm"),
    path("password-reset/complete/",
         PasswordResetCompleteView.as_view(),
         name="password_reset_complete"),

    path("django-admin/", admin.site.urls),

    # Custom Wagtail for added XLSX, JSON and CSV import to olimpiads
    path("admin/home/olimpiad/import/",
         home_views.OlimpiadAdminImportView.as_view(), name="olimpiad-import"),

    # Wagtail
    path("admin/", include(wagtailadmin_urls)),
    path("documents/", include(wagtaildocs_urls)),
    path("search/", search_views.search, name="search"),

    # Home
    path("", home_views.Home.as_view(), name="home"),
    path("register/", home_views.RegisterView.as_view(), name="register"),
    path("contact/", home_views.Contact.as_view(), name="contact"),

    path("test/", home_views.AllTestView.as_view(), name="test-all"),
    path("test/<int:pk>/", home_views.TestView.as_view(), name="test"),

    path("olimpiads/", home_views.OlimpiadsView.as_view(), name="olimpiads"),
    path("olimpiads/<int:pk>/", home_views.OlimpiadView.as_view(),
         name="olimpiad"),

    path("profile/", home_views.ProfileView.as_view(), name="profile"),
    path("profile/edit/", home_views.ProfileEditView.as_view(),
         name="profile-edit"),

    path("marks/create/", home_views.MarkCreateView.as_view(),
         name="mark-create"),
    path("marks/edit/<int:pk>", home_views.MarkUpdateView.as_view(),
         name="mark-edit"),
    path("marks/delete/<int:pk>",
         home_views.MarkDeleteView.as_view(), name="mark-delete"),

    path("advice/", home_views.AdviceView.as_view(), name="advice"),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

urlpatterns = urlpatterns + [
    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    path("", include(wagtail_urls), name="wagtail-home"),
    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    path("pages/", include(wagtail_urls)),
]
