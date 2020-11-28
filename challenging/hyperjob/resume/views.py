from django.shortcuts import render, reverse
from django.views.generic import ListView
from django.views import View
from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from .models import Resume


class ResumeListView(ListView):
    template_name = "resume/resumes.html"
    model = Resume


class CreateResume(View):
    def get(self, request):
        return render(request, 'resume/create.html')

    def post(self, request, **kwargs):
        if not request.user.is_authenticated or request.user.is_staff:
            raise PermissionDenied
        author = request.user
        description = request.POST.get('description')
        Resume.objects.create(description=description, author=author)
        return HttpResponseRedirect(reverse('vacancy:home'))
