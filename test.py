from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

class FlaskTests(TestCase):

    def test_show_home(self):
        with app.test_client() as client:
            res = client.get('/')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3>Time</h3>', html)

    def test_check_word(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['board'] = [['T', 'E', 'S', 'T', 'T'],
                                           ['T', 'E', 'S', 'T', 'T'],
                                           ['T', 'E', 'S', 'T', 'T'],
                                           ['T', 'E', 'S', 'T', 'T'],
                                           ['T', 'E', 'S', 'T', 'T']]

            res = client.post('/word-check', data={'word': 'test'})
            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['result'], 'ok')

    def test_store_data(self):
        with app.test_client() as client:
            with client.session_transaction() as change_session:
                change_session['high_score'] = 5
                change_session['game_count'] = 1
            res = client.post('/store-data', data={'score': 10})


            self.assertEqual(res.status_code, 200)
            self.assertEqual(res.json['high_score'], 10)
            self.assertEqual(res.json['game_count'], 2)

