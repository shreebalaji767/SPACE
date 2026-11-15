import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class StaticSiteTests(unittest.TestCase):
    def test_pages_entry_and_assets_exist(self):
        for path in (
            "index.html", "manifest.json", "sw.js", "icon.svg",
            "tree-menu.html", "static/void-expansion.js",
            "static/void-universe.js", "static/void-3d.js",
            "static/void-relics.js", "static/void-responsive.css",
            "static/void-space-gameplay.webm",
        ):
            self.assertTrue((ROOT / path).is_file(), path)

    def test_index_uses_relative_pages_paths(self):
        html = (ROOT / "index.html").read_text(encoding="utf-8")
        self.assertIn('href="./manifest.json"', html)
        self.assertIn('register("./sw.js")', html)
        self.assertIn('./static/void-expansion.js', html)
        self.assertIn('./static/void-universe.js', html)
        self.assertIn('./static/void-relics.js', html)
        self.assertNotIn('src="/static/', html)
        self.assertNotIn('href="/manifest.json"', html)

    def test_existing_game_modules_are_included(self):
        paths = (
            "index.html", "static/void-expansion.js",
            "static/void-universe.js", "static/void-relics.js",
        )
        source = "\\n".join((ROOT / path).read_text(encoding="utf-8") for path in paths)
        for feature in ("voidSpaceProfile", "voidSpaceExpansion",
                        "voidSpaceUniverse", "voidSpaceRelics",
                        "Campaign", "Boss Rush"):
            self.assertIn(feature, source)

    def test_worker_is_subpath_aware(self):
        worker = (ROOT / "sw.js").read_text(encoding="utf-8")
        self.assertIn("self.registration.scope", worker)
        self.assertIn('new URL("static/void-universe.js", BASE)', worker)

if __name__ == "__main__":
    unittest.main()
