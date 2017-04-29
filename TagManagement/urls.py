from django.conf.urls import url
from . import views
from . import suggest_tags

urlpatterns = [
    url(r'^assignTagsToFile', views.assignTagsToFile, name='assignTagsToFile'),
    url(r'^assignTags', views.assignTags, name='assignTags'),
    url(r'^autoCompleteFilePath', views.autoCompleteFilePath, name='autoCompleteFilepath'),
    url(r'^autoCompleteTags', views.autoCompleteTags, name='autoCompleteTags'),
    url(r'^maintainAssignedTags', views.maintainAssignedTags, name='maintainAssignedTags'),
    url(r'^storeFilePath', views.storeFilePath, name='storeFilePath'),
    url(r'^autoAssign', views.autoAssign, name='autoAssign'),
    url(r'^suggest',views.findSuggestedTags,name='findSuggestedTags'),
    url(r'^notification',views.generateNotification,name='generateNotification'),
    url(r'^test',views.test,name='test'),
    url(r'^addAllToAssignedTags', views.addAllToAssignedTags, name='addAllToAssignedTags'),
    url(r'^removeAssignedTags', views.removeAssignedTags, name='removeAssignedTags'),
  ]

