from django.urls import path
from . import views

app_name = 'git'

urlpatterns = [


    path('/upload', views.GitDisplay.as_view(), name='git-upload'),
    path('/download', views.download, name='download-excel'),   
    path('/fix', views.fix_git, name='fix'),
]


urlpatterns += [
    path('/api/mac-addresses', views.mac_fetcher, name='mac-fetcher'),
    path('/asset-tag', views.asset_tag_fetcher, name='asset-tag'),
    path('/get-git', views.get_git, name='get-git')
]