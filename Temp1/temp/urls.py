from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from . import views as core_views


urlpatterns=[
    url(r'^accounts/profile/$', core_views.home, name='home'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name="login.html"), name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
]
