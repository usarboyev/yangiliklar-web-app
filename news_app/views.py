from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from django.contrib.auth.models import User
from django.db.models import Q
from hitcount.utils import get_hitcount_model
from hitcount.views import HitCountDetailView, HitCountMixin
from .models import News, Category
from .forms import ContactForm, CommentForm
from config.custom_permission import OnlySuperUserLogged


def news_list(request):
    news_list = News.published.all()
    context = {
        'news_list': news_list
    }
    return render(request, 'news/news_list.html', context)


class NewsHitCountDetailView(HitCountDetailView):
    pass

def news_detail(request, news):
    news = get_object_or_404(News, slug=news, status=News.Status.Published)
    context = {}
    # hitcount logic
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hit_context = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request, hit_count)
    if hit_count_response.hit_counted:
        hits += 1
        hit_context['hit_counted'] = hit_count_response.hit_counted
        hit_context['hit_message'] = hit_count_response.hit_message
        hit_context['total_hits'] = hits

    comments = news.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # yangi komment obyektini yaratamiz lekin db ga saqlamaymiz
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            # izoh egasini so'rov yuborayotgan userga bog'ladik
            new_comment.user = request.user
            # db ga saqlaymiz
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    context = {
        'news': news,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form
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


class NewsUpdateView(OnlySuperUserLogged, UpdateView):
    model = News
    fields = ('title', 'body', 'image', 'status','category')
    template_name = 'crud/news_edit.html'


class NewsDeleteView(OnlySuperUserLogged, DeleteView):
    model = News
    template_name = 'crud/news_delete.html'
    success_url = reverse_lazy('home_page')


class NewsCreateView(OnlySuperUserLogged, CreateView):
    model = News
    template_name = 'crud/news_create.html'
    fields = ('title','slug','body','image','category','status')
    prepopulated_fields = {'slug': ('title',)}
    # success_url = reverse_lazy('home_page')

@login_required
@user_passes_test(lambda u: u.is_superuser )
def admin_page_view(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        'admin_users': admin_users
    }
    return render(request, 'pages/admin_page.html', context)


class SearchResultView(ListView):
    model = News
    template_name = 'news/search_result.html'
    context_object_name = 'barcha_yangiliklar'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            # title__icontains=query      # faqat 'title' bo'yicha qidiradi
            Q(title__icontains=query) | Q(body__icontains=query)   # | belgisi 'or' ni bildiradi
        )