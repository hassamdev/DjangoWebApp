"""
URL configuration for Itx_Solution project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from employees import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views




urlpatterns = [
    # path("polls",include("polls.urls")),
    #path('admin/', admin.site.urls),
    path("logout",views._logout,name="logout"),
    path('',views.login_page,name="login_page"),
    path('signUp',views.signUp_page,name="signUp_page"),
    path('after_login',views.after_login_page,name="after_login_page"),
    path('hours',views.hours_page,name="hours_page"),
    path('upload-image',views.upload_image,name="upload_img"),
    path('upload-status',views.upload_status,name="upload_status"),
    path('week-data',views.week_data,name="week_data"),
    path('month-data',views.month_data,name="month_data"),
    path('year-data',views.year_data,name="year_data"),
    path('filter-data',views.filter_data,name="filter_data"),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name ="forgot_password.html"), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name="pass_reset_sent_msg.html"), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="password_reset.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name="pass_reset_complete.html"), name='password_reset_complete'),
    path('auth-app/user',views.auth_app_user,name="auth_app_user"), # this endpoint is for authentiaction of app user
    path('add/app-user',views.add_user_by_app,name="add_user_by_app"), # this endpoint is for adding new user by app.
    path("rfid-auth",views.rfid_auth,name ="rfid_auth") # this endpoint is for authentication of rfid module user
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)