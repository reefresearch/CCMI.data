"""Project-path deployment must preserve executable JavaScript."""
from pathlib import Path
import tempfile
import unittest
from prepare_site import rebase_local_paths


class ProjectPathTests(unittest.TestCase):
    def test_csv_quote_regex_survives_beside_a_rebased_data_request(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'data').mkdir()
            source='''const quote=v=>String(v).replace(/"/g,'""'); fetch('/data/observations.json');'''
            expected='''const quote=v=>String(v).replace(/"/g,'""'); fetch('/CCMI.data/data/observations.json');'''
            self.assertEqual(rebase_local_paths(source,'/CCMI.data',root),expected)

    def test_page_assets_home_and_external_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'app.js').touch()
            source='<a href="/">Home</a><script src="/app.js?v=1"></script><a href="https://example.org/">External</a>'
            expected='<a href="/CCMI.data/">Home</a><script src="/CCMI.data/app.js?v=1"></script><a href="https://example.org/">External</a>'
            self.assertEqual(rebase_local_paths(source,'/CCMI.data',root),expected)


if __name__=='__main__':
    unittest.main()
