"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
COMMON/URLS.py
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from django.conf.urls import url
from . import views     # import from current package

urlpatterns = [
    url(r'^home/$', views.home, name='home'),
    url(r'^store/$', views.store, name='store'),
    url(r'^central/([a-zA-Z0-9_]+)/$', views.central, name='central'),
    url(r'^', views.notfound, name='notfound'),
]





