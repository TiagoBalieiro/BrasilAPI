from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import unittest
import requests

class testesAutomatizados(unittest.TestCase):

    def setUp(self):
        options = Options()
        self.driver = webdriver.Chrome(options=options)

    def test_valid_city_code(self):
        cityCode = 241
        url = f"https://brasilapi.com.br/api/cptec/v1/ondas/{cityCode}"
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('cidade', data)
        self.assertEqual(data['cidade'], 'Rio de Janeiro')

    def test_valid_days(self):
        cityCode = 241
        days = 2
        url = f"https://brasilapi.com.br/api/cptec/v1/ondas/{cityCode}/{days}"
        response = requests.get(url)

        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['ondas']), days)

    def test_invalid_decimal_city_code(self):
        cityCode = 241.5
        url = f"https://brasilapi.com.br/api/cptec/v1/ondas/{cityCode}"
        response = requests.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertIn('Cidade não localizada', response.text)

    def test_invalid_negative_city_code(self):
        cityCode = -1
        url = f"https://brasilapi.com.br/api/cptec/v1/ondas/{cityCode}"
        response = requests.get(url)

        self.assertEqual(response.status_code, 404)
        self.assertIn('Cidade não localizada', response.text)

    def test_invalid_days_less_than_one(self):
        cityCode = 241
        days = 0
        url = f"https://brasilapi.com.br/api/cptec/v1/ondas/{cityCode}/{days}"
        response = requests.get(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Quantidade de dias inválida', response.text)

    def test_invalid_days_greater_than_six(self):
        cityCode = 241
        days = 7
        url = f"https://brasilapi.com.br/api/cptec/v1/ondas/{cityCode}/{days}"
        response = requests.get(url)

        self.assertEqual(response.status_code, 400)
        self.assertIn('Quantidade de dias inválida', response.text)

    def tearDown(self):
        self.driver.quit()


if __name__ == "__main__":
    suite = unittest.TestLoader().loadTestsFromTestCase(testesAutomatizados)
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)
