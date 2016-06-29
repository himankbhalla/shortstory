from django.conf.urls import patterns, include, url, static
import views

#write url mapping below this


urlpatterns = patterns('',

url(r'^login/$', 'mylogin', name='login'),
url(r'^logout/$', 'mylogout', name='logout'),

                       
    
)
