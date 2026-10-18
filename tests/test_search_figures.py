"""Behavioral checks for portable reference discovery and metadata search."""
from pathlib import Path
import csv
import importlib.util
import os
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('search_figures', ROOT/'scripts/search_figures.py')
search = importlib.util.module_from_spec(spec)
spec.loader.exec_module(search)


def write_csv(path, rows):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=sorted({key for row in rows for key in row}))
        writer.writeheader()
        writer.writerows(rows)


class ReferenceSearchTests(unittest.TestCase):
    def test_bundle_is_portable_and_explicit_override_wins(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            bundle = root/'skill/assets/svg-library/manifest.csv'
            other = root/'other/manifest.csv'
            write_csv(bundle, [{'file':'one.svg'}])
            write_csv(other, [{'file':'two.svg'}])
            with patch.object(search, 'SKILL_ROOT', root/'skill'), patch.dict(os.environ, {}, clear=True):
                args = ('FIGURECRAFT_SVG_LIBRARY', Path('svg-library'), Path('unused'), 'svg')
                self.assertEqual(search.discover(None, *args), bundle.resolve())
                self.assertEqual(search.discover(str(other.parent), *args), other.resolve())
                with self.assertRaises(ValueError):
                    search.discover(str(root/'missing'), *args)

    def test_reference_rank_ignores_license_and_raster(self):
        base = dict(title='MLP projection', path='/tmp/mlp.svg', category='neural')
        terms = search.query_terms('MLP')
        hits = [search.rank(dict(base, license=license, has_raster=raster), terms)
                for license, raster in [('CC0', False), ('unknown', True), ('CC BY-ND', False)]]
        self.assertGreater(hits[0]['score'], 0)
        self.assertEqual(len({hit['score'] for hit in hits}), 1)
        unrelated = dict(title='amplpthing', path='/tmp/another.svg', category='other')
        self.assertEqual(search.rank(unrelated, terms)['score'], 0)

    def test_chinese_terms_find_english_metadata(self):
        candidate = dict(title='encoder decoder', path='/tmp/model.svg', category='ml')
        hit = search.rank(candidate, search.query_terms('编码器 解码器'))
        self.assertIn('encoder', hit['matched'])
        self.assertIn('decoder', hit['matched'])

    def test_benchmark_resolves_paths_and_multiline_captions(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            batch = root/'agent_01'
            (batch/'figures').mkdir(parents=True)
            for name in ['one.png', 'two.png']:
                (batch/'figures'/name).touch()
            write_csv(batch/'results.csv', [
                dict(image_path='figures\\one.png', title='model', caption='a, b\nc', status='needs_review'),
                dict(image_path=str((batch/'figures/two.png').resolve()), title='model'),
                dict(image_path='', title='absent'),
            ])
            hits = list(search.benchmark_candidates(root))
            self.assertEqual(len(hits), 2)
            self.assertTrue(all(Path(hit['path']).is_file() for hit in hits))
            self.assertEqual(hits[0]['caption'], 'a, b\nc')
            self.assertEqual(hits[0]['status'], 'needs_review')


if __name__ == '__main__':
    unittest.main()
