from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^browseAndSearch', views.browseAndSearch, name='browseAndSearch'),
    url(r'^getGraphData', views.getGraphData, name='getGraphData'),
    url(r'^getFilteredFiles', views.getFilteredFiles, name='getFilteredFiles')
  ]

