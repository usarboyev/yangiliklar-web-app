from django.urls import path
from .views import (
    news_list, news_detail, ContactPageView, HomePageView,
    LocalNewsPageView, GlobalNewsPageView, SportNewsPageView,
    TechNewsPageView
)

urlpatterns = [
    path('', HomePageView.as_view(), name='home_page'),
    path('news/all/', news_list, name='news_list'),
    path('news/<slug:news>/', news_detail, name='news_detail_page'),
    path('contact/', ContactPageView.as_view(), name='contact_page'),
    path('local/', LocalNewsPageView.as_view(), name='local_news_page'),
    path('global/', GlobalNewsPageView.as_view(), name='global_news_page'),
    path('sport/', SportNewsPageView.as_view(), name='sport_news_page'),
    path('technology/', TechNewsPageView.as_view(), name='tech_news_page')
]


