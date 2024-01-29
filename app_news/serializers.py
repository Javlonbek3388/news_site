from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from .models import News


# class NewsSerializer(ModelSerializer):
#     news_title = SerializerMethodField()
#     news_desc = SerializerMethodField()
#     news_text = SerializerMethodField()
#
#     class Meta:
#         model = News
#         read_only_fields = ('news_views_count',)
#         fields='__all__'
#         extra_kwargs = {
#             'news_title_uz': {'write_only': True},
#             'news_title_en': {'write_only': True},
#             'news_title_ru': {'write_only': True},
#             'news_title': {'read_only': True},
#
#             'news_desc_uz': {'write_only': True},
#             'news_desc_en': {'write_only': True},
#             'news_desc_ru': {'write_only': True},
#             'news_desc': {'read_only': True},
#
#             'news_text_uz': {'write_only': True},
#             'news_text_en': {'write_only': True},
#             'news_text_ru': {'write_only': True},
#             'news_text': {'read_only': True}
#         }
#
#         def get_news_title(self, obj):
#             try:
#                 match self.context['request'].query_params['lang']:
#                     case 'uz':
#                         return obj.news_title_uz
#                     case 'en':
#                         return obj.news_title_en
#                     case 'ru':
#                         return obj.news_title_ru
#                     case _:
#                         return obj.news_title_uz
#             except:
#                 return obj.news_title_uz
#
#         def get_news_desc(self, obj):
#             try:
#                 match self.context['request'].query_params['lang']:
#                     case 'uz':
#                         return obj.news_desc_uz
#                     case 'en':
#                         return obj.news_desc_en
#                     case 'ru':
#                         return obj.news_desc_ru
#                     case _:
#                         return obj.news_desc_uz
#             except:
#                 return obj.news_desc_uz
#
#         def get_news_text(self, obj):
#             try:
#                 match self.context['request'].query_params['lang']:
#                     case 'uz':
#                         return obj.news_text_uz
#                     case 'en':
#                         return obj.news_text_en
#                     case 'ru':
#                         return obj.news_text_ru
#                     case _:
#                         return obj.news_text_uz
#             except:
#                 return obj.news_text_uz

class NewsSerializer(ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
