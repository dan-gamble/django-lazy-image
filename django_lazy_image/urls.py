from django.conf.urls import url

from .views import ImageView

urlpatterns = [
    url(r'thumbnail/(?P<pk>\d+)/(?P<width>\d+|auto)/(?P<height>\d+|auto)/(?P<format>source|jpg|png|webp)/(?P<crop>[^/]+)/(?P<quality>\d+|60)/', ImageView.as_view(), name='thumbnail'),
]
