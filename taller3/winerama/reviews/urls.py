from django.conf.urls import url
#from apps.review.views import user_recommendation_list
from . import views

from django.contrib.auth.views import (
    login, logout, password_reset, password_reset_done, password_reset_confirm,
    password_reset_complete
)
urlpatterns = [
    # ex: /
    url(r'^$', views.review_list, name='review_list'),
    # ex: /review/5/
    url(r'^top/', views.top_list, name='top_list'),
    url(r'^reclist/', views.RecomendationsList, name='top_list2'),
    url(r'^reclistonline/', views.RecomendationsListOnline, name='top_listonline'),
    #url(r'^reclist/', views.RecomendationsListCat, name='top_list2'),
    url(r'^review/(?P<review_id>[0-9]+)/$', views.review_detail, name='review_detail'),
    # ex: /wine/
    url(r'^wine$', views.WineListView.as_view(), name='wine_list'),
    # ex: /wine/5/
    url(r'^wine/(?P<wine_id>[0-9]+)/$', views.wine_detail, name='wine_detail'),
    url(r'^wine/(?P<wine_id>[0-9]+)/add_review/$', views.add_review, name='add_review'),
    # ex: /review/user - get reviews for the logged user
    url(r'^review/user/(?P<username>.+)/$', views.user_review_list, name='user_review_list'),
    # ex: /review/user - get reviews for the user passed in the url
    url(r'^review/user/$', views.user_review_list, name='user_review_list'),
    # ex: /recommendation - get wine recommendations for the logged user
    url(r'^recommendation/$', views.user_recommendation_list, name='user_recommendation_list'),
    url(r'^login/$', login, {'template_name': 'accounts/login.html'}, name='login'),
    url(r'^logout/$', logout, {'template_name': 'accounts/logout.html'}, name='logout'),
    url(r'^reviews/register/$', views.register, name='register'),
]
