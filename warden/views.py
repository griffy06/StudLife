from django.shortcuts import render
from django.views.generic import View


class UserFormView(View):

    template_name = 'warden/warden_login.html'

    def get(self, request):
        return render(request, self.template_name)
