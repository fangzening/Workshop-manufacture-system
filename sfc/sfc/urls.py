"""sfc URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.urls import include
from django.urls import path

from django.contrib.auth import views as auth_views





urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('manufacturing/', include('manufacturing.urls')),
    path('config/git', include('git.urls')),
    path('config/', include('maskconfig.urls',namespace='maskconfig')),
    path('line/', include('line.urls')),
    path('line/', include('rules.urls')),
    path('api/', include('api.urls')),
    path('offline_station/', include('offline_station.urls')),
    path('shipping/', include('shipping.urls')),
    path('qms/', include('qms.urls')),
    path('wms/', include('wms.urls')),
    
]

#Add URL maps to redirect the base URL to our application
from django.views.generic import RedirectView
urlpatterns += [
    path('', RedirectView.as_view(url='manufacturing/', permanent=True)),
]

from django.conf import settings
from django.conf.urls.static import static
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


from django.contrib.auth import views as auth_views
from django.urls import reverse
from django.urls import reverse_lazy
#Add Django site authentication urls (for login, logout, password management)
urlpatterns += [
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(success_url=reverse_lazy('users:password_reset_done')), name='password_reset'),
    path('accounts/', include('django.contrib.auth.urls')),

    # path('password_reset/', auth_views.password_reset, name='password_reset'),
    # path('password_reset/done/', auth_views.password_reset_done, name='password_reset_done'),
    # path('reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    #     auth_views.password_reset_confirm, name='password_reset_confirm'),
    # path('reset/done/', auth_views.password_reset_complete, name='password_reset_complete'),
]


urlpatterns += [

    # Forget Password
    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_formIMS.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             # success_url='/login/'
         ),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_doneIMS.html'
         ),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirmIMS.html'
         ),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_completeIMS.html'
         ),
         name='password_reset_complete'),
]

