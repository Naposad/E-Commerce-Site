from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin

class CustomPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'siteweb/password_change.html'
    success_message = "Votre mot de passe a été modifié avec succès."
    success_url = reverse_lazy('list-product')  # Rediriger après succès
