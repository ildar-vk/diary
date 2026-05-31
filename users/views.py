from django.contrib.auth import login
from django.shortcuts import redirect
from django.views.generic import CreateView
from .models import User

class RegisterView(CreateView):
    model = User
    fields = ['email', 'password']
    template_name = 'registration/register.html'
    success_url = '/'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(self.request, user)
        return redirect(self.success_url)
