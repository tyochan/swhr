from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class CustomLoginView(auth_views.LoginView):
    redirect_authenticated_user = True


class CustomPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'form_change_password.html'

    def get_success_url(self, **kwargs):
        return reverse_lazy('personal_details:update_user', kwargs={'slug': self.request.user.slug})
