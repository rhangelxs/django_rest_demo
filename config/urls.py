from django.conf import settings
from django.urls import include, path, reverse, resolve
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views

from rest_auth.views import LoginView as RestAuthLoginView
from rest_auth.registration.views import RegisterView as RestAuthRegisterView

from django_rest_demo.checkin.views import LocationList, LocationVisit, LocationRatio, UserRatio, VisitList
from django_rest_demo.users.views_rest import UserList

from rest_framework_swagger.views import get_swagger_view

schema_view = get_swagger_view(title='REST API')

urlpatterns = [
    path('', schema_view)
]

urlpatterns += [
                  path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
                  path(
                      "about/",
                      TemplateView.as_view(template_name="pages/about.html"),
                      name="about",
                  ),
                  # Django Admin, use {% url 'admin:index' %}
                  path(settings.ADMIN_URL, admin.site.urls),
                  # User management
                  path(
                      "users/",
                      include("django_rest_demo.users.urls", namespace="users"),
                  ),
                  path("accounts/", include("allauth.urls")),
                  # Your stuff: custom urls includes go here
              ] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

# DRF login pages
urlpatterns += [
    # path("api/", include('rest_framework.urls', namespace="rest_framework")),
    path('rest-auth/', include('rest_auth.urls')),
    path('rest-auth/registration/', include('rest_auth.registration.urls')),

    path('api/register/', RestAuthRegisterView.as_view(), name="rest_register"),
    path('api/sign_in/', RestAuthLoginView.as_view(), name="rest_login"),
    # path('api/users/', UserList.as_view(), name="login"),
]

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('api/users', UserList, base_name='users')

router.register('api/locations', LocationList, base_name='locations')
router.register('api/visits', VisitList, base_name='visits')


urlpatterns += [
    path('api/locations/<int:pk>/visit/', LocationVisit.as_view(), name="location_visit"),
    path('api/locations/<int:pk>/ratio/', LocationRatio.as_view(), name="location_ratio"),
    path('api/users/<int:pk>/ratio/', UserRatio.as_view(), name="user_ratio"),

]

urlpatterns += router.urls

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
