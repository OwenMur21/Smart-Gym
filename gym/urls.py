from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns=[
    url('^$',views.homepage,name = 'home'),
    url(r'^join/(\d+)$',views.join, name = 'join_gym'),
    url(r'^add_gym/$', views.add_gym, name='add_gym'),
    url(r'^add_image/$', views.gym_images, name='add_image'),
    url(r'^edit_gym/(\d+)',views.edit_gym,name="edit_gym"),
    url(r'^exit_gym/(\d+)$', views.exit_gym, name='exit_gym'),
    



]
if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
