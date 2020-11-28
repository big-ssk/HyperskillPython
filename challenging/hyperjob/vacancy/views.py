from django.views.generic import TemplateView, ListView, CreateView
from django.views import View
from django.shortcuts import render, reverse
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Vacancy
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect


# Create your views here.

class MenuView(TemplateView):
    template_name = 'vacancy/menu.html'


class VacancyListView(ListView):
    template_name = "vacancy/vacancies.html"
    model = Vacancy


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = 'login'
    template_name = 'vacancy/signup.html'


class LoginPageView(LoginView):
    form_class = AuthenticationForm
    redirect_authenticated_user = True
    template_name = 'vacancy/login.html'


# class HomepageView(TemplateView):
#     template_name = 'vacancy/home.html'
class HomepageView(View):
    def get(self, request):
        if request.user.is_staff:
            return HttpResponseRedirect(reverse('vacancy:create'))
        return HttpResponseRedirect(reverse('resume:create'))

class CreateVacancy(View):
    def get(self, request):
        return render(request, 'vacancy/create.html')

    def post(self, request, **kwargs):
        if not request.user.is_authenticated or not request.user.is_staff:
            raise PermissionDenied
        author = request.user
        description = request.POST.get('description')
        Vacancy.objects.create(description=description, author=author)
        return HttpResponseRedirect(reverse('vacancy:home'))
