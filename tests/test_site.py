import hashlib
import json
import re
import unittest
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class SiteParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.images = []
        self.ids = set()
        self.refs = []

    def handle_starttag(self, tag, attrs):
        data = dict(attrs)
        if "id" in data:
            self.ids.add(data["id"])
        if tag == "img":
            self.images.append(data)
        if tag == "link" and "href" in data:
            self.refs.append(data["href"])
        if tag == "script" and "src" in data:
            self.refs.append(data["src"])


class ProveinSiteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.html = (ROOT / "index.html").read_text(encoding="utf-8")
        cls.css = (ROOT / "styles.css").read_text(encoding="utf-8")
        cls.sources = json.loads((ROOT / "image-sources.json").read_text(encoding="utf-8"))
        cls.parser = SiteParser()
        cls.parser.feed(cls.html)

    def test_required_files_exist_and_are_nonempty(self):
        for relative in ("index.html", "styles.css", "script.js", "image-sources.json", "README.md"):
            path = ROOT / relative
            self.assertTrue(path.is_file(), relative)
            self.assertGreater(path.stat().st_size, 0, relative)

    def test_page_structure_and_language(self):
        self.assertRegex(self.html, r'<html\s+lang="es"')
        for element in ("<header", "<nav", "<main", "<footer", "<h1"):
            self.assertIn(element, self.html)
        self.assertTrue({"inicio", "servicios", "empresa", "contacto"}.issubset(self.parser.ids))
        self.assertIn('name="viewport"', self.html)

    def test_factual_contact_and_scope(self):
        for text in (
            "Recambios para vehículos industriales",
            "camiones, autocares y remolques",
            "956 141 859",
            "jerez@provein.net",
            "Pol. Industrial Bertola, Nave 27",
            "11408 Jerez de la Frontera, Cádiz",
            "salvo neumáticos",
        ):
            self.assertIn(text, self.html)

    def test_no_prohibited_claims_or_features(self):
        visible = re.sub(r"<[^>]+>", " ", self.html).lower()
        for prohibited in ("en stock", "disponibilidad inmediata", "desde €", "garantía", "nuestros clientes", "inteligencia artificial"):
            self.assertNotIn(prohibited, visible)
        self.assertNotIn("<video", self.html.lower())
        self.assertNotIn("<iframe", self.html.lower())

    def test_all_six_approved_images_are_used_and_present(self):
        declared = self.sources["images"]
        self.assertEqual(6, len(declared))
        used = {image.get("src") for image in self.parser.images}
        for image in declared:
            relative = image["file"]
            self.assertIn(relative, used)
            self.assertTrue((ROOT / relative).is_file(), relative)

    def test_asset_hashes_match_manifest(self):
        for image in self.sources["images"]:
            digest = hashlib.sha256((ROOT / image["file"]).read_bytes()).hexdigest()
            self.assertEqual(image["sha256"], digest, image["file"])

    def test_images_have_dimensions_alt_and_no_upscale_contract(self):
        declared = {image["file"]: image for image in self.sources["images"]}
        for image in self.parser.images:
            self.assertTrue(image.get("alt") is not None)
            self.assertIn("width", image)
            self.assertIn("height", image)
            source = declared[image["src"]]
            limit_width = source.get("display_limit_width", source["width"])
            self.assertLessEqual(int(image["width"]), limit_width)
            self.assertLessEqual(int(image["height"]), source.get("source_height", source["height"]))
        self.assertIn("max-width: 720px", self.css)
        self.assertIn("max-width: 640px", self.css)
        self.assertIn("max-width: 282px", self.css)

    def test_local_styles_and_script_resolve(self):
        for ref in self.parser.refs:
            if not ref.startswith(("http://", "https://", "//")):
                self.assertTrue((ROOT / ref).is_file(), ref)

    def test_responsive_and_accessible_navigation(self):
        self.assertIn("@media (max-width: 820px)", self.css)
        self.assertIn('aria-expanded="false"', self.html)
        self.assertIn('aria-controls="nav"', self.html)
        self.assertIn('href="#contenido"', self.html)


if __name__ == "__main__":
    unittest.main()
