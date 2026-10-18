"""Verify distributed assets, attribution metadata and byte integrity."""
from pathlib import Path
import csv
import hashlib
import re
import unittest
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]/'assets/svg-library'


class BundledLibraryTests(unittest.TestCase):
    def test_manifest_and_assets(self):
        with (ROOT/'manifest.csv').open(encoding='utf-8-sig', newline='') as stream:
            rows = list(csv.DictReader(stream))
        self.assertEqual(len(rows), 2405)
        self.assertEqual(len({row['file'] for row in rows}), len(rows))
        for row in rows:
            with self.subTest(asset=row['file']):
                path = (ROOT/row['file']).resolve()
                self.assertTrue(path.is_relative_to(ROOT.resolve()))
                data = path.read_bytes()
                self.assertEqual(hashlib.sha256(data).hexdigest(), row['sha256'])
                xml = ET.fromstring(data)
                self.assertEqual(xml.tag, '{http://www.w3.org/2000/svg}svg')
                for element in xml.iter():
                    self.assertNotEqual(element.tag.rsplit('}', 1)[-1], 'script')
                    self.assertFalse(any(re.fullmatch(r'on[a-z]+', key.lower()) for key in element.attrib))
                self.assertTrue(row['author'] and row['page_url'] and row['license'])
                license = row['license'].upper()
                expected = ('T3-attribution-sharealike' if 'BY-SA' in license else
                            'T2-attribution' if 'CC BY' in license else 'T1-permissive')
                self.assertEqual(row['tier'], expected)
        for filename in ['README.md', 'gallery.html', 'THIRD_PARTY_NOTICES.md',
                         'licenses/devicon-MIT.txt', 'licenses/tabler-MIT.txt',
                         'licenses/material-design-icons.txt', 'licenses/tensorflow-Apache-2.0.txt']:
            self.assertTrue((ROOT/filename).is_file(), filename)


if __name__ == '__main__':
    unittest.main()
