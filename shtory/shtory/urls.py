from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'shtory.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
 #url(r'^', include('Myuser.urls')),
    url(r'^login/', 'Myuser.views.mylogin', name='mylogin'),
    url(r'^home/$', 'Myuser.views.home', name='home'),
    url(r'^logout/', 'Myuser.views.mylogout', name='mylogout'),
    url(r'^profile/', 'Myuser.views.profile', name='profile'),
    url(r'^addprofile/', 'Myuser.views.addinfo', name='addinfo'),
url(r'^users/(?P<user_id>[\d]+)/$','Myuser.views.show_user_id',name='show_user_id'),
	 url(r'^addprofilepic/$', 'Myuser.views.addprofilepic', name='addprofilepic'), 
	 url(r'^delprofilepic/$', 'Myuser.views.delprofilepic', name='delprofilepic'),
	 url(r'^sign_up/', ('Myuser.views.register_user')),
     url(r'^register_success/', ('Myuser.views.register_success')),
     url(r'^accounts/confirm/(?P<activation_key>\w+)/', ('Myuser.views.register_confirm')),
 url(r'^addrelation/(?P<user_id>[\d]+)/$', 'Myuser.views.add_relationship', name='add_relationship'),	
 url(r'^delrelation/(?P<user_id>[\d]+)/$', 'Myuser.views.remove_relationship', name='remove_relationship'),	
 url(r'^get_followers/$', 'Myuser.views.get_followers', name='get_followers'),
 url(r'^get_following/$', 'Myuser.views.get_following', name='get_following'),	
 url(r'^feed/$', 'Myuser.views.home', name='home'),
	

#urls for Story app starts below this line

url(r'^addcomment/', 'Story.views.addcomment', name='addcomment'),	
url(r'^delcomment/', 'Story.views.delete_comment', name='delete_comment'),	
url(r'^editcomment/', 'Story.views.edit_comment', name='edit_comment'),	

url(r'^addstory/', 'Story.views.addstory', name='addstory'),
url(r'^delete_story/', 'Story.views.delete_story', name='delete_story'),
url(r'^edit_story/', 'Story.views.edit_story', name='edit_story'),
url(r'^vote_story/', 'Story.views.vote_story', name='vote_story'),
url(r'^book_story/', 'Story.views.book_story', name='book_story'),


url(r'^userstory/', 'Story.views.userstory', name='userstory'),
url(r'^followerstory/', 'Story.views.followerstory', name='followerstory'),
url(r'^bookmark/', 'Story.views.bookmark', name='bookmark'),
url(r'^searchquery/', 'Story.views.tagsearch', name='search'),
     #url(r'^tagsearch/$', 'appusers.views.tagsearch', name='search'),

#url(r'^fav_stories/', 'Story.views.fav_stories', name='fav_stories'),


url(r'^reportstory/$', 'Story.views.reportstory', name='reportstory'),                  



) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

