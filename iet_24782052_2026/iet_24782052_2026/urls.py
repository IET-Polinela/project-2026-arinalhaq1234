from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from usermanagement_24782052.api_views import RegisterView
from usermanagement_24782052 import views as user_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('dashboard/', include('dashboard_24782052.urls')),

    path('api/', include('main_app.api_urls')),

    path('api/register/', RegisterView.as_view(), name='api_register'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('login/', user_views.CustomLoginView.as_view(), name='login'),
    path('logout/', user_views.CustomLogoutView.as_view(), name='logout'),
    path('register/', user_views.register, name='register'),
]