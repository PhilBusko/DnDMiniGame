"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
CFB-SITE URLS
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

from django.conf.urls import include, url
from django.contrib import admin

import dnd4e.views as DV
import webscraper.views as WV


dnd4e_url = [
    url(r'^intro/', DV.intro, name="intro"),
    url(r'^corerules/', DV.corerules, name="corerules"),
    url(r'^resources/', DV.resources, name="resources"),
    url(r'^magicitems/', DV.magicitems, name="magicitems"),
    url(r'^encgroup/', DV.encgroup, name="encgroup"),
    url(r'^domainraces/', DV.domainraces, name="domainraces"),
    url(r'^monst_stats/', DV.monst_stats, name="monst_stats"),
    url(r'^miniatures/', DV.miniatures, name="miniatures"),
    url(r'^terrain/', DV.terrain, name="terrain"),
    url(r'^database/', DV.database, name="database"),
    
    url(r'^db_edit/([a-zA-Z0-9_]+)/$', DV.db_edit, name="db_edit"),
    url(r'^db_report/([a-zA-Z0-9_]+)/$', DV.db_report, name="db_report"),

    url(r'^', DV.intro, name="intro"),
]


webscraper_url = [
    url(r'^scraper/$', WV.scraper, name='scraper'),
    url(r'^scraper_jx/([a-zA-Z0-9_]+)/$', WV.scraper_jx, name='scraper_jx'),

    url(r'^', WV.scraper, name='scraper'),
]

urlpatterns = [
    url(r'^dnd4e/', include(dnd4e_url, namespace='dnd4e')),
    url(r'^webscraper/', include(webscraper_url, namespace='webscraper')),

    url(r'^admin/', admin.site.urls),
]

