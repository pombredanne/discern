from django.conf.urls import *

urlpatterns=patterns('django.contrib.auth.views',
                     url(r'^login/$','login'),
                     url(r'^logout/$','logout'),
                     )

urlpatterns +=patterns('grader.views',
                       url(r'^register/$','register'),
                       url(r'^$','index'),
                       )
