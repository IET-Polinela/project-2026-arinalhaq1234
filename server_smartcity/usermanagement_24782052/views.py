from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect, render
from django.urls import reverse_lazy

from .forms import CustomUserCreationForm


class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

    def form_valid(self, form):
        messages.success(self.request, 'Login berhasil.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Username atau password salah.')
        return super().form_invalid(form)

    def get_success_url(self):
        return '/reports/'


class CustomLogoutView(LogoutView):
    next_page = '/'

    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Logout berhasil.')
        return super().dispatch(request, *args, **kwargs)


def register(request):
    if request.user.is_authenticated:
        return redirect('/reports/')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            messages.success(request, 'Registrasi berhasil. Silakan login.')
            return redirect('login')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def register_view(request):
    return register(request)