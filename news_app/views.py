from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy

from .models import News, Category
from .forms import ContactForm
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView


def news_list(request):
    news_list = News.published.all()
    context = {
        'news_list': news_list
    }
    return render(request, 'news/news_list.html', context)


def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {
        'news': news
    }
    return render(request, 'news/news_detail.html', context)


# def home_page(request):
#     categories = Category.objects.all()
#     news_list = News.published.all().order_by('-publish_time')[:5]
#     local_one = News.published.filter(category__name='Mahalliy').order_by('-publish_time')[:1]
#     local_news = News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[1:5]
#     context = {
#         'news_list': news_list,
#         'categories': categories,
#         'local_one': local_one,
#         'local_news': local_news
#     }
#     return render(request, 'news/index.html', context)


class HomePageView(ListView):
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['news_list'] = News.published.all().order_by('-publish_time')[:5]
        context['local_news'] = News.published.all().filter(category__name='Mahalliy').order_by('-publish_time')[:5]
        context['global_news'] = News.published.all().filter(category__name='Xorij').order_by('-publish_time')[:5]
        context['sport_news'] = News.published.all().filter(category__name='Sport').order_by('-publish_time')[:5]
        context['technology_news'] = News.published.all().filter(category__name='Texnologiya').order_by('-publish_time')[:5]
        return context


class ContactPageView(TemplateView):
    template_name = 'news/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == 'POST' and form.is_valid():
            form.save()
            return HttpResponse('<h1>Thank you!</h1>')
        context = {
            'form': form
        }
        return render(request, 'news/contact.html', context)


class LocalNewsPageView(ListView):
    model = News
    template_name = 'news/local_news.html'
    context_object_name = 'local'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Mahalliy')
        return news


class GlobalNewsPageView(ListView):
    model = News
    template_name = 'news/global_news.html'
    context_object_name = 'global'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Xorij')
        return news


class TechNewsPageView(ListView):
    model = News
    template_name = 'news/technology_news.html'
    context_object_name = 'technology'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Texnologiya')
        return news


class SportNewsPageView(ListView):
    model = News
    template_name = 'news/sport_news.html'
    context_object_name = 'sport'

    def get_queryset(self):
        news = self.model.published.all().filter(category__name='Sport')
        return news

class NewsUpdateView(UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'status','category')
    template_name = 'crud/news_edit.html'


class NewsDeleteView(DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title','slug','body','image','category','status')
    prepopulated_fields = {'slug': ('title',)}
    # success_url = reverse_lazy('home_page')