from django.shortcuts import render
from django.views.generic import View


class UserFormView(View):

    template_name = 'canteen/canteen_login.html'

    def get(self, request):
        return render(request, self.template_name)
