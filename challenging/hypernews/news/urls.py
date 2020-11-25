from django.urls import path
from . import views

urlpatterns = [
    path('', views.coming_soon, name='coming_soon'),
    path('news/', views.index, name='index'),
    path('news/<int:link>/', views.article, name='article'),
    path('news/create/', views.Create.as_view(), name="create")
]