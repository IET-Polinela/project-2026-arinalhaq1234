from django.contrib import admin
from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)

from django_scalar.views import scalar_viewer
from usermanagement_24782052.api_views import RegisterView
from usermanagement_24782052 import views as user_views


urlpatterns = [
    path("admin/", admin.site.urls),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),

    path(
    'api/docs/swagger/',
    SpectacularSwaggerView.as_view(url_name='schema'),
    name='swagger-ui',
    ),

    path('api/docs/scalar/', scalar_viewer, name='scalar-ui'),
    
    # Halaman Django biasa
    path("", include("main_app.urls")),
    path("about/", include("about.urls")),
    path("contacts/", include("contacts.urls")),
    path("dashboard/", include("dashboard_24782052.urls")),

    # Endpoint REST API
    path("api/", include("main_app.api_urls")),

    # Autentikasi API JWT
    path("api/register/", RegisterView.as_view(), name="api_register"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    # Autentikasi halaman Django biasa
    path("login/", user_views.CustomLoginView.as_view(), name="login"),
    path("logout/", user_views.CustomLogoutView.as_view(), name="logout"),
    path("register/", user_views.register, name="register"),
]