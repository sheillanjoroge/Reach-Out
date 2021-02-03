from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'login$', views.logIn, name='login'),
    url(r'^$', views.home, name='home'),
    url(r'register$', views.register, name='register'),
    url(r'announce/', views.announcement, name='announce'),
    url(r'announce/new/', views.create_announcement, name='new-announcement'),
    url(r'^profile$', views.profile, name='profile'),
    url(r'^blog/$', views.blog, name='blog'),
    url(r'^business/$', views.business, name='business'),
    url(r'^business/(\d+)$', views.selected_business, name='selected_business'),
    url(r'^new/business/$', views.create_business, name='add-business'),
    url(r'^essential/$', views.essential, name='essential'),
    url(r'^meeting/$', views.meeting, name='meeting'),
    url(r'^meeting/(\d+)$', views.selected_meeting, name='selected_meeting'),
    url(r'^essential/(\d+)$', views.selected_essential, name='selected_essential'),
    url(r'^search/', views.search_results, name='search_results'),
]

if settings.DEBUG:
    urlpatterns+= static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
