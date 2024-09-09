from http import HTTPStatus

from django.test import TestCase
from django.urls import reverse_lazy, reverse

from women.models import Women


class GetPagesTestCase(TestCase):

    fixtures = ['women_women.json', 'women_categories.json', 'women_husband.json', 'women_tags.json']

    def setUp(self):
        pass

    def test_mainpage(self):
        path = reverse_lazy('home')
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTemplateUsed(response, 'women/index.html')
        self.assertEqual(response.context_data['title'], 'Главная страница')

    def test_redirect_addpage(self):
        path = reverse('addpost')
        reverse_uri = reverse('users:login') + '?next=' + path
        response = self.client.get(path)
        self.assertEqual(response.status_code, HTTPStatus.FOUND)
        self.assertRedirects(response, reverse_uri)

    def test_data_mainpage(self):
        path = reverse('home')
        w = Women.published.all().select_related('cat')
        response = self.client.get(path)
        self.assertQuerysetEqual(w[:5], response.context_data['posts'])

    def test_paginate_mainpage(self):
        paginate_by = 5
        page = 3
        path = reverse('home') + f'?page={page}'
        w = Women.published.all().select_related('cat')
        response = self.client.get(path)
        self.assertQuerysetEqual(response.context_data['posts'], w[(page-1)*paginate_by:page*paginate_by])

    def test_content_post(self):
        w = Women.published.get(pk=1)
        path = reverse('post', args=[w.slug])
        response = self.client.get(path)
        self.assertEqual(w.content, response.context_data['post'].content)

    def tearDown(self):
        pass
