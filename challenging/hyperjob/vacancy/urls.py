from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import MenuView, VacancyListView, LoginPageView, SignUpView, HomepageView, CreateVacancy


app_name = 'vacancy'

urlpatterns = [
    path('', MenuView.as_view(), name='menu'),
    path('vacancies/', VacancyListView.as_view(), name='vacancies'),
    path('login', LoginPageView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('signup', SignUpView.as_view(), name='signup'),
    path('home/', HomepageView.as_view(), name='home'),
    path('vacancy/new', CreateVacancy.as_view(), name='create')
]
