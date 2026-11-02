"""Check catalogue completeness, source equivalence and local distribution links."""
from pathlib import Path
from urllib.parse import urlparse,unquote
import hashlib,json,sys

ROOT=Path(__file__).resolve().parent
dist=ROOT/'site' if (ROOT/'site').exists() else ROOT/'dist'
catalog=json.loads((dist/'catalog.json').read_text())
files=json.loads((dist/'file-catalog.json').read_text())
series=json.loads((dist/'data/icon-timeseries.json').read_text())['series']
assert len(catalog)==24, len(catalog)
assert len(files)==1122, len(files)
assert len(series)==8, len(series)
assert sum(len(s['rows']) for s in series if s.get('site_id')=='mf')==20380
assert sum(len(s['rows']) for s in series if s.get('site_id')=='icon')==85299
for d in catalog:
    assert (dist/'records'/(d['id']+'.html')).exists(),d['id']
    assert (dist/'metadata'/d['metadata']).exists(),d['metadata']
    if d.get('hobo'):
        for name in d['aliases']:
            assert (ROOT/'sources/hobo'/name).read_bytes()==(dist/'files'/name).read_bytes()
for f in files:
    assert (dist/'metadata'/f['metadata']).exists(),f['metadata']
    assert (dist/'metadata'/f['metadata_json']).exists(),f['metadata_json']
    if not f.get('external'):
        path=urlparse(f['url']).path
        # Accept a configured project prefix, preserving data paths and names.
        for folder in ['files','data','code']:
            marker='/'+folder+'/'
            if marker in path:
                local=dist/folder/unquote(path.split(marker,1)[1])
                assert local.is_file(),local
                if f.get('checksum_type')=='sha256':
                    assert hashlib.sha256(local.read_bytes()).hexdigest()==f['checksum'],local
                break
        else:raise AssertionError(f['url'])
assert not (ROOT/'.openai').exists()
# A source checkout normally contains .git; only published assets must exclude it.
assert not (dist/'.git').exists()
assert 'CCMI.data' in (dist/'app.js').read_text()
print(f'PASS: {len(catalog)} records; {len(files):,} files; {len(series)} logger series; original hashes and metadata verified.')
