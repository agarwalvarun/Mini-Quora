from django.conf.urls import url,include
from .views import login,home, logout, forgot_password, reset_password, activate
urlpatterns = [
	url(r'^(?P<id>\d+)/home/$',home, name = 'home'),
	url(r'^logout/$',logout, name = 'logout'),
	url(r'^forgot-password/$', forgot_password, name = 'forgot_password'),
    url(r'^reset/(?P<id>\d+)/(?P<otp>\d{4})/$', reset_password, name = 'reset_password'),
    url(r'^activate/(?P<id>\d+)/(?P<otp>\d{4})/$', activate, name = 'activate_account'),
]