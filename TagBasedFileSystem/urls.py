from django.conf.urls import include, url
from django.contrib import admin
from TagManagement import views as tagviews
#from restaurant import views
admin.autodiscover()
urlpatterns =[
    # Examples:
    # url(r'^$', 'TagBasedFileSystem.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^$', tagviews.index ),
	url(r'^tag/', include('TagManagement.urls')),
    url(r'^search/', include('FileSearch.urls')),
    url(r'^admin/', include(admin.site.urls)),

    
]
