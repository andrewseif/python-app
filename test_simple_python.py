import unittest
import requests


class SimplePythonAppTest(unittest.TestCase):
    def test_hello_world_endpoint(self):
        response = requests.get('http://localhost:8080/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message": "Hello World"})

    def test_health_endpoint(self):
        response = requests.get('http://localhost:8080/health')
        self.assertEqual(response.status_code, 200)
        self.assertIn(response.json()['status'], ['success', 'failure'])


if __name__ == '__main__':
    unittest.main()
