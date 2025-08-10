from django.test import TestCase
from django.urls import resolve, reverse

from cidadao import views


class CidadaoURLsTest(TestCase):
    def test_cidadaoCreate_url_is_corrent(self):
        url=reverse('cidadao:add-cidadao')
        self.assertEqual(url,'/cidadao/create/cidadao/')

    def test_cidadaoUpdate_url_is_corrent(self):
        url=reverse('cidadao:edit-cidadao', kwargs={'id': 1})
        self.assertEqual(url,'/cidadao/update/1/cidadao/')
    
    def test_cidadaoDetail_url_is_corrent(self):
        url=reverse('cidadao:detail-cidadao', kwargs={'pk': 1})
        self.assertEqual(url,'/cidadao/detail/1/cidadao/')

class CidadaoViewsTest(TestCase):
   
    def test_cidadaoCreate_view_funcition_is_corrent(self):
        view=resolve(reverse('cidadao:add-cidadao'))
        self.assertIs(view.func,views.cidadaoCreate)

    def test_cidadaoUpdate_view_funcition_is_corrent(self):
        view=resolve(reverse('cidadao:edit-cidadao', kwargs={'id':2}))
        self.assertIs(view.func,views.cidadaoUpdate)