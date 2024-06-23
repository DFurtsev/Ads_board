from django.urls import path, include
from .views import *
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('ads/', AdsList.as_view(), name='ads'),
    path('ads/<int:pk>', AdDetail.as_view(), name='ad_detail'),
    path('ads/create/', AdCreate.as_view(), name='ad_create'),
    path('ads/<int:pk>/edit/', AdUpdate.as_view(), name='ad_update'),
    path('ads/myads/', MyAds.as_view(), name='my_ads'),
    path('ads/responses/', Responses.as_view(), name='responses_for_me'),
    path('ads/responses/<int:pk>/reject/', RejectResponses.as_view(), name='reject'),
    path('confirm', ConfirmEmail.as_view(), name='confirmation'),

]