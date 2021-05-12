from django.urls import reverse, resolve

import pytest
'''
    path('checkssn', views.checkssn, name='checkssn'),
    path('scankeypart', views.scankeypart, name='scankeypart'),
    path('testssn', views.testssn, name='testssn'),
    path('checkkeypart', views.checkkeypart, name='checkkeypart'),
    path('getpart', views.getpart, name='getpart'),
'''
class TestUrls:

    def test_checkssn_url(self):
        path = reverse('api:checkssn')
        assert resolve(path).view_name == 'api:checkssn'

    def test_scankeypart_url(self):
        path = reverse('api:scankeypart')
        assert resolve(path).view_name == 'api:scankeypart'

    def test_testssn_url(self):
        path = reverse('api:testssn')
        assert resolve(path).view_name == 'api:testssn'

    def test_checkkeypart_url(self):
        path = reverse('api:checkkeypart')
        assert resolve(path).view_name == 'api:checkkeypart'
        
    def test_getpart_url(self):
        path = reverse('api:getpart')
        assert resolve(path).view_name == 'api:getpart'


'''
@pytest.mark.django_db

class TestModels:

    def test_model(self):
        Mask = mixer.blend('maskconfig:Mask',id=1)
        assert rule.

'''