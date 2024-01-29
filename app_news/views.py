import jwt
from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import News
from .serializers import NewsSerializer
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView




class NewsListApiView(ListAPIView):
    permission_classes = (AllowAny, )
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsCreateApiView(CreateAPIView):
    permission_classes = (IsAuthenticated, )
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsUpdateApiView(UpdateAPIView):
    permission_classes = (AllowAny, )
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsRetrieveApiView(RetrieveAPIView):
    permission_classes = (AllowAny, )
    queryset = News.objects.all()
    serializer_class = NewsSerializer


class NewsDeleteApiView(DestroyAPIView):
    permission_classes = (AllowAny, )
    queryset = News.objects.all()
    serializer_class = NewsSerializer







# class NewsModelViewSet(ModelViewSet):
#     serializer_class = NewsSerializer
#     queryset = News.objects.all()
#
#     def create(self, request, *args, **kwargs):
#         try:
#             token = self.request.META['HTTP_TOKEN']
#         except:
#             raise AuthenticationFailed('Send token, please')
#
#         if not token:
#             raise AuthenticationFailed('Invalid token, login again, please')
#
#         try:
#             payload = jwt.decode(token, 'secret', algorithms=['HS256'])
#             print(payload)
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Token expired, login again, please')
#         except:
#             raise AuthenticationFailed('Invalid token, login again, please')
#
#         user = get_user_model().objects.filter(username=payload['username']).first()
#         request.data['news_author'] = user.id
#
#         return super().create(request, *args, **kwargs)
#
#     def retrieve(self, request, *args, **kwargs):
#         try:
#             counter = News.objects.filter(pk=self.kwargs['pk']).values_list('news_views_count').first()[0]
#             # print(counter)
#             News.objects.filter(pk=self.kwargs['pk']).update(news_views_count=counter +1)
#         except:
#             pass
#         return super().retrieve(request, *args, **kwargs)
