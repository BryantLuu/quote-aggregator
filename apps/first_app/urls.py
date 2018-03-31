from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'login$', views.login),
    url(r'^quotes$', views.quotes),
    url(r'^create_quote$', views.create_quote),
    url(r'^users/(?P<id>\d+)$', views.profile),
    url(r'^add_favorite$', views.add_favorite),
    url(r'^remove_favorite$', views.remove_favorite),
    url(r'^log_out$', views.log_out),
]
