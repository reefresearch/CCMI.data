"""Build linked study/file records from captured, public repository inventories.

No external data bytes are mirrored. GitHub links are commit-pinned; Zenodo
links use exact record versions; ENA supplies accession-specific FASTQ links.
"""
from pathlib import Path
from urllib.parse import quote
import hashlib, html, json, re

CHECKED='2026-10-29'

def clean(value):
    return ' '.join(html.unescape(re.sub('<[^>]+>', '', str(value or ''))).split())

def role(name):
    s=name.lower()
    if s.endswith(('.fastq.gz','.fq.gz','.fastq','.fq')): return 'sequence'
    if s.endswith(('.zip','.tar.gz','.tgz')): return 'archive'
    if s.endswith(('.r','.rmd','.py','.ipynb')) or 'nurserycode' in s or ('code' in s and s.endswith('.docx')): return 'code'
    if Path(s).name.startswith(('readme','sessioninfo','license')) or s.endswith(('.pdf','.rtf','.md','.docx','.html')): return 'documentation'
    return 'data'

def file_category(name,kind,primary):
    if kind=='code' or (kind=='archive' and 'schul' in name.lower()): return 'code'
    if any(s in name.lower() for s in ['temp','sst','dhw','licor']): return 'environmental'
    return primary

def augment(catalog,root,dist,origin):
    read=lambda name:json.loads((root/'sources'/name).read_text())
    config=read('studies.json')
    github={r['repo']:r for r in read('github-inventory.json')}
    datacite={r['id']:r['metadata'] for r in read('datacite.json') if r.get('metadata')}
    papers={r['doi']:r['metadata'] for r in read('papers.json') if r.get('metadata')}
    projects={r['id']:r for r in read('ena-runs.json')}
    zfiles=read('zenodo-files.json')
    tag=read('disease-tag.json')
    meta=dist/'metadata'; (meta/'file-records').mkdir(exist_ok=True)
    total_files=[]

    def attach(parent,name,url,provider,version=None,size=None,checksum=None,checksum_type=None,source_url=None,kind=None,category=None,**extra):
        kind=kind or role(name)
        ident='ccmi-file-'+hashlib.sha256((parent['id']+'\n'+url).encode()).hexdigest()[:16]
        f={'id':ident,'parent_id':parent['id'],'name':name,'title':Path(name).name,'url':url,'repository_url':source_url or parent.get('repository_url') or origin+parent['landing'],
           'provider':provider,'version':version or parent.get('version'),'kind':kind,'category':category or file_category(name,kind,parent['category']),
           'format':'FASTQ.GZ' if name.lower().endswith('.fastq.gz') else (Path(name).suffix[1:].upper() or 'FILE'),'size_bytes':size,
           'checksum':checksum,'checksum_type':checksum_type,'source_license':parent.get('license'),
           'paper_doi':parent.get('paper_doi'),'dataset_doi':parent.get('dataset_doi'),'concept_doi':parent.get('concept_doi'),
           'doi_scope':'Dataset DOI belongs to the parent deposit; this file has no separately registered DOI.',
           'landing':'/?file='+ident,'metadata':'file-records/'+ident+'.meta.md','metadata_json':'file-records/'+ident+'.json',
           'metadata_checked':CHECKED,'link_status':'Listed in source inventory; full file transfer not tested.','external':parent.get('external',False),**extra}
        if parent.get('coordinates'):
            for k in ['coordinates','latitude','longitude','location','coordinate_basis','coordinate_source','coordinate_source_url','coordinate_scope','coordinate_uncertainty_m','coordinate_datum']:f[k]=parent.get(k)
        parent.setdefault('files',[]).append(f); total_files.append(f)
        return f

    # Include canonical local distributions without duplicating byte-identical aliases.
    for parent in catalog:
        parent.update(paper_doi=None,dataset_doi=None,concept_doi=None,categories=[parent['category']])
        if parent['category']=='code':
            attach(parent,'ingest.py',origin+'/code/ingest.py','CCMI',size=(dist/'code/ingest.py').stat().st_size,checksum=parent['sha256'],checksum_type='sha256',kind='code')
            attach(parent,'requirements.txt',origin+'/code/requirements.txt','CCMI',size=(dist/'code/requirements.txt').stat().st_size,kind='documentation')
        else:
            name=parent['aliases'][0]
            attach(parent,name,origin+'/files/'+quote(name),'CCMI',size=parent['bytes'],checksum=parent['sha256'],checksum_type='sha256')
            attach(parent,parent['csv'],origin+'/data/'+quote(parent['csv']),'CCMI',size=(dist/'data'/parent['csv']).stat().st_size,checksum=parent['csv_sha256'],checksum_type='sha256')

    for cfg in config:
        p=papers.get(cfg.get('paper_doi'),{})
        d=datacite.get(cfg.get('zenodo'),{})
        creators=[x.get('name') for x in d.get('creators',[]) if x.get('name')]
        paper_authors=[clean(x.get('given','')+' '+x.get('family','')) for x in p.get('author',[])]
        licence=next((x.get('rights') for x in d.get('rightsList',[]) if x.get('rightsIdentifier')),None)
        parent={'id':cfg['id'],'external':True,'category':'ecological','title':cfg['title'],'description':cfg['description'],
                'paper_doi':cfg.get('paper_doi'),'paper_title':clean((p.get('title') or [cfg['title']])[0]),'paper_authors':paper_authors,
                'paper_year':cfg.get('year'),'paper_relationship_status':cfg.get('paper_relationship_status','Linked by the paper data-availability statement or repository README.'),
                'dataset_doi':'10.5281/zenodo.'+cfg['zenodo'] if cfg.get('zenodo') else cfg.get('dryad'),
                'concept_doi':next((x['relatedIdentifier'] for x in d.get('relatedIdentifiers',[]) if x['relationType']=='IsVersionOf'),None),
                'dataset_creators':creators,'dataset_title':clean((d.get('titles') or [{'title':cfg['title']}])[0]['title']),
                'repository_url':'https://zenodo.org/records/'+cfg['zenodo'] if cfg.get('zenodo') else 'https://doi.org/'+cfg['dryad'] if cfg.get('dryad') else 'https://github.com/'+cfg['github'] if cfg.get('github') else 'https://www.ncbi.nlm.nih.gov/bioproject/'+cfg['project'],
                'repository_accession':cfg.get('project'),'source_repositories':[],'license':licence,'license_url':next((x.get('rightsUri') for x in d.get('rightsList',[]) if x.get('rightsIdentifier')),None),
                'version':d.get('version') or ('record '+cfg['zenodo'] if cfg.get('zenodo') else None),
                'status':'External deposit','metadata_status':'Repository-derived; scientific metadata review pending','metadata_checked':CHECKED,
                'variables':[],'format':[],'files':[],'aliases':[],'depth':None,'coordinates':None,'location':cfg.get('location'),'start':None,'end':None,'records':None,
                'creator':creators or None,'contact':None,'doi':None,'notes':[],
                'metadata':cfg['id']+'.meta.md','landing':'/records/'+cfg['id']+'.html'}
        if cfg.get('zenodo'):
            zid=cfg['zenodo']; zurl='https://zenodo.org/records/'+zid
            parent['source_repositories'].append({'provider':'Zenodo','url':zurl,'dataset_doi':parent['dataset_doi']})
            for name,digest in zfiles[zid]:
                # Preserve exact listed digest; some repository displays omit leading zeroes.
                valid=bool(re.fullmatch('[0-9a-f]{32}',digest))
                attach(parent,name,zurl+'/files/'+quote(name,safe='/')+'?download=1','Zenodo',version='record '+zid,
                       checksum=digest if valid else None,checksum_type='md5' if valid else None,source_url=zurl,
                       repository_checksum_display=digest,inventory_source=zurl,
                       checksum_note=None if valid else 'Displayed checksum is not 32 hexadecimal characters; verify at source before use.')
        if cfg.get('github') or cfg.get('github_tag'):
            g=github[cfg['github']] if cfg.get('github') else tag
            repo=g['repo']; commit=g['commit']; repo_url='https://github.com/'+repo
            parent['source_repositories'].append({'provider':'GitHub','url':repo_url,'commit':commit,'tag':g.get('tag')})
            parent['github_commit']=commit
            if not parent['version']: parent['version']=commit
            if not parent['dataset_creators']:parent['dataset_creators']=[repo.split('/')[0]+' (repository owner; not a verified authorship statement)']
            for f in g['files']:
                path=f['path']; path_enc=quote(path,safe='/')
                attach(parent,path,'https://raw.githubusercontent.com/'+repo+'/'+commit+'/'+path_enc,'GitHub',version=commit,size=f.get('size'),
                       source_url=repo_url+'/blob/'+commit+'/'+path_enc,git_blob_sha1=f['sha'],commit=commit,
                       source_license=(g.get('meta',{}).get('license') or {}).get('spdx_id'),
                       inventory_source='https://api.github.com/repos/'+repo+'/git/trees/'+commit+'?recursive=1')
            if not (g.get('meta',{}).get('license') or {}).get('spdx_id'):
                parent['notes'].append('The GitHub repository does not declare a licence in its metadata. Public access alone does not establish reuse permission.')
        if cfg.get('project'):
            project=cfg['project']; manifest=projects[project]
            parent['source_repositories'].append({'provider':'NCBI / ENA','url':'https://www.ncbi.nlm.nih.gov/bioproject/'+project,'accession':project,'inventory_url':manifest['url']})
            parent['sequence_runs']=len(manifest['runs'])
            for run in manifest['runs']:
                urls=run.get('fastq_ftp','').split(';');digests=run.get('fastq_md5','').split(';');sizes=run.get('fastq_bytes','').split(';')
                for i,url in enumerate(urls):
                    if not url:continue
                    attach(parent,url.rsplit('/',1)[-1],'https://'+url,'ENA',version=run['run_accession'],size=int(sizes[i]) if i<len(sizes) and sizes[i] else None,
                           checksum=digests[i] if i<len(digests) and digests[i] else None,checksum_type='md5',
                           source_url='https://www.ncbi.nlm.nih.gov/sra/'+run['run_accession'],kind='sequence',category='ecological',
                           run_accession=run['run_accession'],sample_accession=run['sample_accession'],project_accession=project,
                           inventory_source=manifest['url'],source_license=None,
                           source_note='FASTQ distribution supplied by ENA; NCBI SRA run and BioProject identifiers retained.')
            parent['notes'].append('All ENA-listed runs under the linked BioProject are indexed. Confirm the article-specific sample subset before combining or analysing files. ENA serves the linked FASTQ copies; NCBI remains linked at project and run level.')
        if cfg.get('dryad'):
            dd=read('dryad-datacite.json'); rights=dd.get('rightsList',[])
            parent['license']=next((x.get('rights') for x in rights if x.get('rightsIdentifier')),None)
            parent['license_url']=next((x.get('rightsUri') for x in rights if x.get('rightsIdentifier')),None)
            parent['dataset_creators']=[x['name'] for x in dd.get('creators',[]) if x.get('name')]
            parent['version']='2022-11-17 repository version'
            parent['source_repositories'].append({'provider':'Dryad','url':'https://doi.org/'+cfg['dryad'],'dataset_doi':cfg['dryad']})
            attach(parent,'disease_deepnursery_apr2022_longformat_dryad.csv','https://datadryad.org/downloads/file_stream/1934971','Dryad',source_url='https://doi.org/'+cfg['dryad'])
            attach(parent,'README.rtf','https://datadryad.org/downloads/file_stream/1934969','Dryad',source_url='https://doi.org/'+cfg['dryad'],kind='documentation')
        parent['categories']=sorted(set(['ecological']+[f['category'] for f in parent['files']]))
        parent['format']=sorted(set(f['format'] for f in parent['files']))
        parent['aliases']=[f['name'] for f in parent['files']]
        parent['notes'].extend(['Files are linked at the original host; data.ccmi does not mirror external data bytes.',
                                'File roles and categories are inferred from names and repository context. Data dictionaries, temporal coverage, units and quality flags have not been transcribed or independently audited.',
                                'Named regions are descriptive. No precise coordinates are inferred or plotted.'])
        if cfg.get('paper_relationship_status'):parent['notes'].append(cfg['paper_relationship_status'])
        parent['schema']={'@context':'https://schema.org','@type':'Dataset','identifier':parent['dataset_doi'] or parent.get('repository_accession') or parent['id'],
                          'name':parent['title'],'description':parent['description'],'url':origin+parent['landing'],
                          'sameAs':parent['repository_url'],'citation':'https://doi.org/'+parent['paper_doi'] if parent.get('paper_doi') else None,
                          'version':parent['version'],'distribution':[{'@type':'DataDownload','name':f['name'],'encodingFormat':f['format'],'contentUrl':f['url']} for f in parent['files']]}
        if parent['license_url']:parent['schema']['license']=parent['license_url']
        parent['doi']=parent['dataset_doi']
        catalog.append(parent)
        (meta/(parent['id']+'.json')).write_text(json.dumps(parent['schema'],indent=2,ensure_ascii=False))
        front={k:parent.get(k) for k in ['id','title','category','categories','paper_doi','paper_title','paper_authors','paper_year','paper_relationship_status','dataset_doi','concept_doi','dataset_title','dataset_creators','repository_url','repository_accession','license','license_url','version','location','coordinates','start','end','metadata_checked','metadata_status']}
        md='---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in front.items())+'\n---\n\n# '+parent['title']+'\n\n'+parent['description']+'\n\n## Linked files\n\n| File | Role | Category | Host | Exact version |\n| --- | --- | --- | --- | --- |\n'
        for f in parent['files']:md+='| ['+f['name'].replace('|','\\|')+']('+f['url']+') | '+f['kind']+' | '+f['category']+' | '+f['provider']+' | '+str(f['version'] or 'not documented')+' |\n'
        md+='\n## Provenance and use\n\n'+'\n'.join('- '+n for n in parent['notes'])+'\n\n## FAIR readiness\n\nFindable: separate paper, dataset and concept DOI fields, repository accessions, searchable file entries and parent relationships. Accessible: direct HTTPS source links plus repository landing pages. Interoperable: JSON-LD, JSON and Markdown metadata; source units and dictionaries require review. Reusable: retain source licence, creator statements, exact versions and repository checksums where reported. Null values are unverified, not inferred. Full file transfers and scientific validity have not been tested.\n'
        (meta/parent['metadata']).write_text(md)

    for f in total_files:
        parent=next(d for d in catalog if d['id']==f['parent_id'])
        filemeta={**f,'parent_title':parent['title'],'parent_landing':origin+parent['landing'],'paper_title':parent.get('paper_title'),
                  'paper_relationship_status':parent.get('paper_relationship_status'),'units':None,'data_dictionary':None,
                  'temporal_coverage':None,'scientific_quality_control':'Not independently assessed','role_basis':'filename, extension and repository context'}
        (meta/f['metadata_json']).write_text(json.dumps(filemeta,indent=2,ensure_ascii=False))
        fm='---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in filemeta.items())+'\n---\n'
        fm+='\n# '+f['name']+'\n\nFile of ['+parent['title']+']('+origin+parent['landing']+').\n\n## Access and citation\n\n[Open the file]('+f['url']+') · [Source record]('+f['repository_url']+'). Cite the paper and parent dataset separately. A dataset DOI in this record identifies the containing deposit, not this individual file.\n\n## FAIR readiness\n\nThe file has a stable local catalog ID, parent-study relation, source link, source version and reported integrity fields where available. Git blob SHA-1 values identify Git objects, not raw-file SHA-256 checksums. Units, variable definitions, sample subset and scientific quality control must be checked against the original README, paper and repository metadata. Null fields remain unverified. No external data bytes are mirrored.\n'
        (meta/f['metadata']).write_text(fm)
    (dist/'file-catalog.json').write_text(json.dumps(total_files,indent=2,ensure_ascii=False))
    return catalog
