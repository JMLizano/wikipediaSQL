import unittest
from wikipediasql.app import create_app

app = create_app(config_object='tests.settings')


class HomeTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(self):
      self.client = app.test_client()

    def test_home_get(self):
      resp = self.client.get('/')
      self.assertEqual(200, resp.status_code)

    def test_home_post(self):
      resp = self.client.post('/', data=dict(
          query="select * from page limit 20"
      ))
      self.assertEqual(200, resp.status_code)
    
    def test_home_empty_query(self):
      resp = self.client.post('/')
      self.assertEqual(400, resp.status_code)

    def test_home_bad_query(self):
      resp = self.client.post('/', data=dict(
          query="slct * from page limit 20"
      ))
      self.assertEqual(400, resp.status_code)
    
    def test_home_not_allowed(self):
      resp = self.client.post('/', data=dict(
          query="drop table page"
      ))
      self.assertEqual(401, resp.status_code)


class OutdatedTestCase(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
      self.client = app.test_client()

    def test_outdated_get(self):
        resp = self.client.get('/outdated')
        self.assertEqual(200, resp.status_code)
    
    def test_outdated_post(self):
      resp = self.client.post('/outdated', data=dict(
          category="Communes in Martinique"
      ))
      self.assertEqual(200, resp.status_code)
    
    def test_outdated_empty_query(self):
      resp = self.client.post('/outdated')
      self.assertEqual(400, resp.status_code)
    

if __name__ == '__main__':
    unittest.main(verbosity=2)