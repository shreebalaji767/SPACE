import unittest

from app import app


class VoidSpaceSmokeTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def test_home_serves_game_and_expansion(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"VOID SPACE", response.data)
        self.assertIn(b"/static/void-expansion.js", response.data)

    def test_expansion_asset_is_served(self):
        response = self.client.get("/static/void-expansion.js")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"VOID COMMAND DECK", response.data)
        self.assertIn(b"mothership", response.data)

    def test_pwa_endpoints(self):
        self.assertEqual(self.client.get("/manifest.json").status_code, 200)
        self.assertEqual(self.client.get("/icon.svg").status_code, 200)
        self.assertEqual(self.client.get("/sw.js").status_code, 200)

    def test_health_endpoint(self):
        self.assertEqual(self.client.get("/health").data, b"VOID SPACE ONLINE")


if __name__ == "__main__":
    unittest.main()
