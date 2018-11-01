from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.homepage,name = 'home'),
    url(r'^add_gym/$', views.add_gym, name='add_gym'),
    url(r'^edit_gym/(\d+)',views.edit_gym,name="edit_gym"),


]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
