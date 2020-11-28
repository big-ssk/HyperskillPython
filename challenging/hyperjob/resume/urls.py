from django.urls import path
from .views import CreateResume

app_name = 'resume'

urlpatterns = [
    path('new', CreateResume.as_view(), name='create')
]
