import itertools

from django.shortcuts import render, reverse
import json
import random
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
NEWS_JSON_PATH = os.path.join(os.path.dirname(BASE_DIR), 'news.json')

# Create your views here.
with open(NEWS_JSON_PATH) as file:
    file = json.load(file)
    articles = sorted(file, key=lambda i: i['created'], reverse=True)


def coming_soon(request):
    return HttpResponseRedirect(reverse("index"))


def index(request, q=None):
    q = request.GET.get('q')
    if q:
        data = list(filter(lambda x: q in x['title'], articles))
    else:
        data = articles
    return render(request, 'news/index.html', {"articles": data, "q": q})




def article(request, link):
    file = dict(*filter(lambda x: x['link'] == link, articles))
    return render(request, 'news/article.html', {"file": file})


class Create(View):
    def get(self, request):
        return render(request, 'news/create.html')

    def post(self, request):
        text = request.POST.get('text')
        title = request.POST.get('title')
        record = {"created": datetime.now().strftime('%Y-%-m-%-d %H:%M:%S'),
                  "text": text,
                  "title": title,
                  "link": random.randint(100, 10000)}
        articles.append(record)

        return HttpResponseRedirect(reverse("index"))
