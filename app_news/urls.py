from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import NewsListApiView, NewsCreateApiView, NewsUpdateApiView, NewsDeleteApiView, NewsRetrieveApiView

urlpatterns = [
    path('list/', NewsListApiView.as_view(), name='news-list'),
    path('create/', NewsCreateApiView.as_view(), name='news-create'),
    path('update/<int:pk>/', NewsUpdateApiView.as_view(), name='news-update'),
    path('delete/<int:pk>/', NewsDeleteApiView.as_view(), name='news-delete'),
    path('retrieve/<int:pk>/', NewsRetrieveApiView.as_view(), name='news-retrieve'),

]

