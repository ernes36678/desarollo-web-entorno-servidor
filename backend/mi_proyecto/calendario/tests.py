from django.test import TestCase
from django.urls import reverse


class CalendarioTests(TestCase):
    def test_fecha_valida_muestra_sus_detalles(self):
        response = self.client.get(reverse('calendario:calendario', args=['20-10-2026']))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'calendario/fecha.html')
        self.assertTemplateUsed(response, 'template.html')
        self.assertContains(response, '20 de octubre del año 2026')

    def test_fecha_invalida_muestra_pagina_de_error(self):
        response = self.client.get(reverse('calendario:calendario', args=['31-02-2026']))

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'calendario/error.html')
        self.assertTemplateUsed(response, 'template.html')
        self.assertContains(response, 'DD-MM-AAAA', status_code=400)

    def test_fecha_con_formato_incorrecto_muestra_pagina_de_error(self):
        response = self.client.get(reverse('calendario:calendario', args=['1-2-2026']))

        self.assertEqual(response.status_code, 400)
        self.assertTemplateUsed(response, 'calendario/error.html')
