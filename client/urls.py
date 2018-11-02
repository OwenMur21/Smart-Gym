from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.client_home,name = 'client_home'),
    url('^newchatroom/$', views.newchatroom, name='newchatroom'),
    url('^chatrooms/$', views.chatrooms, name='chatrooms'),
    url('^post/(\w+)$', views.post, name='post'),
    url('^chatroom/(\w+)$', views.chatroom, name='chatroom'),

]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
