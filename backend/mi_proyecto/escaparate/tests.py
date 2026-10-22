from django.test import TestCase
from django.urls import reverse


class SitePagesTests(TestCase):
    def test_homepage_uses_shared_template(self):
        response = self.client.get(reverse('core:homepage'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertTemplateUsed(response, 'template.html')
        self.assertContains(response, 'Bienvenido a mi sitio web')

    def test_escaparate_uses_shared_template(self):
        response = self.client.get(reverse('escaparate:homepage'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'escaparate/escaparate.html')
        self.assertTemplateUsed(response, 'template.html')
        self.assertContains(response, 'Sección de escaparate')

    def test_contact_page_includes_simple_form(self):
        response = self.client.get(reverse('core:contacto'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'contacto.html')
        self.assertTemplateUsed(response, 'template.html')
        self.assertContains(response, '<form')
        self.assertContains(response, 'type="email"')
        self.assertContains(response, 'textarea')
