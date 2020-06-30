from django.conf.urls import url 
from events import views 
 
urlpatterns = [ 
    url(r'^api/events$', views.event_list),
    url(r'^api/events/(?P<pk>[0-9]+)$', views.event_detail)
]