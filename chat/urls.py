from django.conf.urls import url
from . import views
from .views import *

urlpatterns = [

    url(r'^$',views.login.as_view(),name='login'),
    url(r'home/$',views.home.as_view(),name='home'),
    url(r'register$',views.register.as_view(),name='register'),
    url(r'dialog/(?P<uid>[0-9]+)/$',views.dialog.as_view(),name='dialog'),
    url(r'logout/$',views.logout_view.as_view(),name='logout'),
    # url(r'messages/$',views.messages,name='messages'),
    url(r'getmessages/$',views.getmessages,name='getmessages'),
]
