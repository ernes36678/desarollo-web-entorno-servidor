from django.test import TestCase
from django.urls import reverse


class TresEnRayaHomepageTests(TestCase):
    def test_homepage_is_accessible(self):
        response = self.client.get(reverse('tres_en_raya:tres_en_raya'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tres_en_raya/tres_en_raya.html')
        self.assertContains(response, '/static/tres_en_raya/css/tres_en_raya.css')
        self.assertContains(response, '<h1>Tres en raya</h1>', html=True)
        self.assertContains(response, 'action="/tres-en-raya/"')
        self.assertEqual(response.content.count(b'type="submit"'), 9)
        self.assertEqual(response.context['tablero'], ['-'] * 9)
        self.assertEqual(response.context['turno'], 'X')
        self.assertEqual(response.context['mensaje'], 'Turno de X')
        self.assertFalse(response.context['terminado'])

    def test_post_updates_board_and_switches_turn(self):
        response = self.client.post(
            reverse('tres_en_raya:tres_en_raya'),
            {'tablero': repr(['-'] * 9), 'turno': 'X', 'posicion': '4'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tablero'], ['-', '-', '-', '-', 'X', '-', '-', '-', '-'])
        self.assertEqual(response.context['turno'], 'O')
        self.assertEqual(response.context['mensaje'], 'Turno de O')

    def test_post_to_occupied_cell_keeps_turn(self):
        response = self.client.post(
            reverse('tres_en_raya:tres_en_raya'),
            {'tablero': repr(['X'] + ['-'] * 8), 'turno': 'O', 'posicion': '0'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tablero'], ['X'] + ['-'] * 8)
        self.assertEqual(response.context['turno'], 'O')
        self.assertEqual(response.context['mensaje'], '¡Casilla ocupada! Elige otra.')

    def test_post_rejects_invalid_move_data(self):
        response = self.client.post(
            reverse('tres_en_raya:tres_en_raya'),
            {'tablero': 'not a board', 'turno': 'X', 'posicion': '0'},
        )

        self.assertEqual(response.status_code, 400)

    def test_post_detects_win_and_offers_restart(self):
        tablero = ['X', 'X', '-', 'O', 'O', '-', '-', '-', '-']
        response = self.client.post(
            reverse('tres_en_raya:tres_en_raya'),
            {'tablero': repr(tablero), 'turno': 'X', 'posicion': '2'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['tablero'][:3], ['X', 'X', 'X'])
        self.assertEqual(response.context['mensaje'], '¡El jugador X ha ganado!')
        self.assertTrue(response.context['terminado'])
        self.assertNotContains(response, 'name="posicion"')
        self.assertContains(response, 'Volver a jugar')
        self.assertContains(response, 'href="/tres-en-raya/"')

    def test_post_detects_draw_and_offers_restart(self):
        tablero = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', '-']
        response = self.client.post(
            reverse('tres_en_raya:tres_en_raya'),
            {'tablero': repr(tablero), 'turno': 'X', 'posicion': '8'},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['mensaje'], '¡Empate!')
        self.assertTrue(response.context['terminado'])
        self.assertContains(response, 'Volver a jugar')
