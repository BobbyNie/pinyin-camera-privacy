import hashlib
import json
from html.parser import HTMLParser
from pathlib import Path
import unittest
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'docs/subscription-v1'


class Page(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.links = []
        self.lang = None
        self.viewport = False
        self.scripts = []
        self.feed(source)

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == 'html':
            self.lang = attrs.get('lang')
        if tag == 'meta' and attrs.get('name') == 'viewport':
            self.viewport = True
        if tag == 'script':
            self.scripts.append(attrs)
        for key in ('href', 'src'):
            if attrs.get(key):
                self.links.append(attrs[key])


class SubscriptionPagesTests(unittest.TestCase):
    def test_existing_production_files_are_byte_identical(self):
        baseline = json.loads((ROOT / 'tests/production-pages-sha256.json').read_text())
        self.assertGreater(len(baseline), 10)
        for name, digest in baseline.items():
            with self.subTest(file=name):
                self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(), digest)

    def test_independent_pages_exist_and_local_links_stay_in_namespace(self):
        for suffix, language in [('', 'zh-CN'), ('-hk', 'zh-HK')]:
            for name in ['marketing', 'support', 'privacy', 'terms']:
                path = SITE / f'{name}{suffix}.html'
                with self.subTest(page=path.name):
                    source = path.read_text()
                    parsed = Page(source)
                    self.assertEqual(parsed.lang, language)
                    self.assertTrue(parsed.viewport)
                    self.assertFalse(parsed.scripts)
                    self.assertIn('2026', source)
                    self.assertIn('bobbynie@gmail.com', source)
                    for link in parsed.links:
                        target = urlsplit(link)
                        if target.scheme or link.startswith('#'):
                            continue
                        resolved = (path.parent / target.path).resolve()
                        self.assertTrue(resolved.is_relative_to(SITE.resolve()), link)
                        self.assertTrue(resolved.exists(), link)
        self.assertTrue((SITE / 'index.html').is_file())

    def test_billing_disclosures_and_apple_management_links(self):
        for suffix, labels in [('', ['符合资格', '自动续订', '永久使用权']),
                               ('-hk', ['符合資格', '自動續訂', '永久使用權'])]:
            for name in ['marketing', 'support', 'terms']:
                source = (SITE / f'{name}{suffix}.html').read_text()
                with self.subTest(page=f'{name}{suffix}'):
                    for label in labels + ['7', '8', '24', 'Apple']:
                        self.assertIn(label, source)
                    self.assertIn('https://apps.apple.com/account/subscriptions', source)
                    self.assertIn('https://reportaproblem.apple.com/', source)
                    self.assertIn('https://www.apple.com/legal/internet-services/itunes/dev/stdeula/', source)
                    for obsolete in ['一次买断', '一次買斷', '完全离线', '完全離線', '保证退款', '保證退款']:
                        self.assertNotIn(obsolete, source)

    def test_privacy_explains_apple_network_without_uploading_learning_images(self):
        for suffix in ['', '-hk']:
            source = (SITE / f'privacy{suffix}.html').read_text()
            for label in ['Apple', 'StoreKit', 'OCR', '2026', 'bobbynie@gmail.com']:
                self.assertIn(label, source)
            self.assertIn('本机' if not suffix else '本機', source)
            self.assertIn('联网' if not suffix else '連網', source)
            self.assertTrue((SITE / ('privacy_hk.txt' if suffix else 'privacy.txt')).is_file())


if __name__ == '__main__':
    unittest.main()
