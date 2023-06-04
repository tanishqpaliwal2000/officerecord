"""officerecord URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
# from django.contrib import admin
from django.urls import path
from . import views
urlpatterns = [
    path('',views.login),
    path('signup',views.signup),
    path('home',views.index,name='index'),
    path('all_emp',views.all_emp,name='all_emp'),
    path('add_emp',views.add_emp,name='add_emp'),
    path('remove_emp',views.remove_emp,name='remove_emp'),
    path('remove_emp/<int:emp_id>', views.remove_emp, name='remove_emp'),
    path('enter_email',views.enter_email),
    path('forgotpassword',views.forgotpassword),
    path('resetpassword',views.resetpassword),

    path('filter_emp',views.filter_emp,name='filter_emp'),
]
'''
accounts/password_reset/ [name='password_reset']
accounts/password_reset/done/ [name='password_reset_done']
accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
accounts/reset/done/ [name='password_reset_complete']
'''