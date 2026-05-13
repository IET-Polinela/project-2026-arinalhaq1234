from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('main_app.urls')),
    path('about/', include('about.urls')),
    path('contacts/', include('contacts.urls')),
    path('dashboard/', include('dashboard_24782052.urls')),

    path('api/', include('main_app.api_urls')),

    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
]