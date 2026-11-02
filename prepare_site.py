"""Create a portable deployment copy; keep dist and original file identifiers intact."""
from pathlib import Path
from urllib.parse import urlparse
import argparse, json, re, shutil, zipfile

ROOT=Path(__file__).resolve().parent
LEGACY_ORIGIN='https://ccmi-research-data.g-roff.chatgpt.site'

def prepare(output='site', origin='', base_path=''):
    target=(ROOT/output).resolve()
    if target != ROOT/'site':
        raise ValueError('Output must be the generated site/ directory.')
    origin=origin.rstrip('/')
    if origin:
        parsed=urlparse(origin)
        if parsed.scheme not in ['http','https'] or not parsed.netloc or parsed.path not in ['', '/']:
            raise ValueError('--origin must be an HTTP(S) origin without a path.')
    base_path=('/'+base_path.strip('/')) if base_path.strip('/') else ''
    if base_path and not re.fullmatch(r'/[A-Za-z0-9._/-]+',base_path):
        raise ValueError('Unsupported base path.')
    if '..' in base_path.split('/'):
        raise ValueError('Parent traversal is not a base path.')
    if target.exists():shutil.rmtree(target)
    shutil.copytree(ROOT/'dist',target)
    for path in target.rglob('*'):
        if not path.is_file() or path.suffix.lower() not in ['.html','.js','.json','.css','.md','.svg']:continue
        text=path.read_text()
        if base_path:
            text=re.sub(r'''(["'`])/(?!/)(?=[A-Za-z0-9_?"'`])''',lambda m:m[1]+base_path+'/',text)
            text=re.sub(r'url\(/(?!/)',lambda m:'url('+base_path+'/',text)
        text=text.replace(LEGACY_ORIGIN,origin+base_path)
        path.write_text(text)
    with zipfile.ZipFile(target/'metadata/ccmi-metadata.zip','w',zipfile.ZIP_DEFLATED) as archive:
        for path in sorted((target/'metadata').rglob('*')):
            if path.suffix in ['.md','.json']:archive.write(path,str(path.relative_to(target/'metadata')))
    (target/'.nojekyll').touch()
    return target

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--origin',default='',help='e.g. https://organisation.github.io (no path)')
    parser.add_argument('--base-path',default='',help='e.g. /ccmi-data for a GitHub project site')
    args=parser.parse_args()
    print(prepare(origin=args.origin,base_path=args.base_path))
