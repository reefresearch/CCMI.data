"""Build the static catalog and one metadata record for every original input."""
from pathlib import Path
import json, re, shutil, hashlib, zipfile
ROOT=Path(__file__).resolve().parent
DIST=ROOT/'dist'; ORIGIN='https://ccmi-research-data.g-roff.chatgpt.site'
for folder in ['metadata','files','code','records']: (DIST/folder).mkdir(exist_ok=True)
inventory=json.loads((DIST/'data/inventory.json').read_text())
catalog=[]
ICON_LOCATION={'coordinates':[19.69960,-80.06058],'latitude':19.69960,'longitude':-80.06058,
 'location':'ICON nursery series, Little Cayman — ICON Reef site reference',
 'coordinate_basis':'Published ICON Reef monitoring-site coordinate, assigned to the ICON nursery series by the data steward on 2026-10-30. Exact nursery-frame and logger positions are unverified.',
 'coordinate_source':'Foster & Foster (2018), Demographics and Population Dynamics Project the Future of Hard Coral Assemblages in Little Cayman, Table 1.',
 'coordinate_source_url':'https://www.scirp.org/journal/paperinformation?paperid=82210',
 'coordinate_scope':'shared site reference; not an individual deployment position',
 'coordinate_uncertainty_m':None,'coordinate_datum':'WGS84 assumed for mapping; source datum not stated'}

policy='''# CCMI Research Data: FAIR implementation policy (draft)

Status: proposed operational policy, pending institutional approval. Created 2026-10-29.

## Findable
Give each dataset a stable local identifier, a versioned landing page, rich metadata,
keywords and machine-readable Schema.org Dataset JSON-LD. Register a persistent
identifier (e.g. DOI through an established repository) before calling a record
fully FAIR. Local identifiers and hosted URLs are not registered DOIs.

## Accessible
Describe access conditions in the metadata and retrieve files through HTTPS.
Keep metadata available when data are restricted or withdrawn, with a tombstone
and reason. This seed site is private; it does not establish public accessibility.
No public release or reuse licence is implied by uploading a file here.

## Interoperable
Preserve original workbooks. Offer timestamped rows as CSV and metadata as JSON
and Markdown. Record variable definitions, units, timezone, missing-value rules,
instrument and provenance. Use ISO 8601 dates and WGS84 (EPSG:4326) coordinates
when verified. Map terms to CF/NERC vocabularies after scientific review; do not
assign seawater_temperature until deployment context confirms that measurement.
Retain both original column names and any approved standardized names.

## Reusable
Record creators, ORCIDs, rights holder, contact, explicit licence, collection
methods, calibration, deployment windows, quality flags, funding, permits,
processing history, version, checksum and suggested citation. Unknown fields
remain null, never inferred as verified. Pre/post-deployment observations must
be screened by the data steward. Light in lux is illuminance, not PAR.

## Release checklist
- Confirm authorship, rights holder, contact and permissions.
- Confirm site coordinates, coordinate precision, nominal depth and deployment dates.
- Resolve instrument changes and mismatches between observation sheets and Details.
- Document calibration, sensor accuracy, clock checks, missingness and quality flags.
- Review variable terms and publish a data dictionary and processing provenance.
- Choose an explicit data/code licence with the rights holder.
- Register a DOI, approve a citation and deposit a versioned preservation copy.
- Arrange steward ownership, backups, retention and metadata persistence.

This is FAIR-aligned preparation, not certification of FAIR compliance.
Reference: https://www.gofair.foundation/fair-principles
'''
(DIST/'metadata/FAIR_POLICY.md').write_text(policy)
for n,r in enumerate(inventory,1):
    depth=int(re.search(r'(18|22|26|30)',r['source'])[1])
    did=f'ccmi-env-{n:03d}'
    variables=['Temperature']+(['Light'] if len(r['headers'])>3 else [])
    title=f'ICON {depth} m — '+('temperature & light' if len(variables)>1 else 'temperature')
    if depth in [26,30]: title+=' · '+('Apr–Oct' if r['start'][5:7]=='04' else 'Jun–Jul' if r['end'][5:7]=='07' else 'Jul–Oct')
    notes=['Original observations are not quality controlled. Individual deployment positions and actual in-water deployment windows require confirmation.','Nominal depth is inferred from the filename; instrument depth is unverified.']
    if r['details']: notes.append('Device Details describe an export segment; the Data sheet may contain edits or appended observations. Do not extend instrument attribution beyond the documented segment without confirmation.')
    if any(r['missing'][2:]): notes.append('Missing measurements occur in timestamped rows; see per-variable counts. Blank cells remain empty in CSV.')
    if depth==18: notes.append('Initial temperatures reach 35.756 °C. Confirm deployment timing and screen handling/air exposure before ecological interpretation.')
    notes.append('Light values are illuminance in lux; no PAR conversion has been applied.') if len(variables)>1 else None
    description=f"Logger observations labelled ICON at nominal {depth} m. The populated observation rows span {r['start'][:10]} to {r['end'][:10]}, with {r['records']:,} timestamped records and a modal sampling interval of {r['interval_minutes']:g} minutes. Deployment location and quality control require steward review."
    dictionary=[]
    for i,h in enumerate(r['headers']):
        name=['Sample index','Observation time','Temperature','Illuminance'][i]
        unit=['1','UTC−05:00','°C','lux'][i]
        dictionary.append({'column':h,'definition':name,'unit':unit,'missing':r['missing'][i],'valid_count':r['records']-r['missing'][i]})
    item={'id':did,'category':'environmental','title':title,'description':description,'depth':depth,'depth_basis':'filename only, unverified','variables':variables,'start':r['start'],'end':r['end'],'records':r['records'],'interval':r['interval_minutes'],'timezone':r['timezone'],'format':['XLSX','CSV'],'status':'Steward review','coordinates':None,'location':None,'license':None,'creator':None,'contact':None,'doi':None,'version':'0.1.0-draft','instrument':r['details'].get('Product','Not documented'),'serial':r['details'].get('Serial Number','10383248 (header)' if depth==18 else 'Not documented'),'sheets':r['sheets'],'dictionary':dictionary,'notes':notes,'aliases':r['aliases'],'sha256':r['sha256'],'bytes':r['bytes'],'csv':r['csv'],'csv_sha256':r['csv_sha256'],'metadata':f'{r["source"]}.meta.md','landing':f'/records/{did}.html','details':r['details'],'timestamp_duplicates':r['duplicate_timestamps'],'non_monotonic_steps':r['non_monotonic_steps']}
    item.update(ICON_LOCATION)
    notes.append(ICON_LOCATION['coordinate_basis'])
    for filename in r['aliases']:
        shutil.copy2(ROOT/'seed'/filename,DIST/'files'/filename)
        fm={'identifier':did,'title':title,'category':'environmental','metadata_status':'draft','metadata_version':'0.1.0','metadata_created':'2026-10-29','source_file':filename,'source_sha256':r['sha256'],'equivalent_files':r['aliases'],'landing_page':ORIGIN+item['landing'],'persistent_identifier':None,'creators':None,'rights_holder':None,'contact':None,'license':None,'access':'owner-private seed repository; release pending steward approval','nominal_depth_m':depth,'depth_verified':False,'latitude':None,'longitude':None,'spatial_reference':'EPSG:4326 when coordinates verified','temporal_start':r['start'].replace(' ','T')+'-05:00','temporal_end':r['end'].replace(' ','T')+'-05:00','temporal_basis':'populated observation timestamps, not confirmed in-water period','sampling_interval_minutes_mode':r['interval_minutes'],'instrument_product_in_details':item['instrument'],'instrument_serial_in_details_or_header':item['serial'],'keywords':['environmental','ICON','temperature']+(['illuminance'] if 'Light' in variables else []),'quality_control':'not applied','related_csv':f'../data/{r["csv"]}'}
        fm.update(ICON_LOCATION)
        fm['spatial_reference']='EPSG:4326 assumed for mapping; source datum not stated'
        md='---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in fm.items())+'\n---\n\n# '+title+'\n\n'+description+'\n\n## Provenance and equivalence\n\nImported without modifying original bytes. SHA-256 identifies both supplied names as byte-identical copies, not separate versions. The CSV retains original headers, timestamp strings and every timestamped row; rows without a timestamp are excluded. No averaging, timezone conversion, unit conversion, interpolation or quality filtering is applied. Data and device-summary date ranges may differ.\n\n## Data dictionary\n\n| Original column | Definition | Units | Populated | Missing |\n| --- | --- | --- | ---: | ---: |\n'
        for d in dictionary: md+=f"| {d['column']} | {d['definition']} | {d['unit']} | {d['valid_count']} | {d['missing']} |\n"
        md+='\n## Quality and interpretation\n\n'+'\n'.join('- '+s for s in notes)+f"\n- Duplicate timestamps: {r['duplicate_timestamps']}; non-increasing timestamp steps: {r['non_monotonic_steps']}.\n"
        md+='\n## Methods and instruments\n\n'+'Instrument metadata below are reproduced from the workbook Details sheet or header and require confirmation against deployment records.\n\n```json\n'+json.dumps(r['details'],indent=2)+'\n```\n'
        md+='\n## Citation and rights\n\nDraft citation: [Creator pending]. (2026). '+title+' (draft version 0.1.0). CCMI Research Data. Local identifier: '+did+'. A DOI and final citation have not been assigned. Data ownership, authorship and licence require confirmation. No open reuse licence is granted.\n\n## FAIR readiness\n\n- Findable: local identifier, landing page, catalog indexing and rich metadata supplied; DOI registration pending.\n- Accessible: HTTPS distribution in private site; release conditions require approval and metadata retention must be operationally guaranteed.\n- Interoperable: original XLSX, CSV, JSON-LD and variable dictionary supplied; controlled vocabulary review pending.\n- Reusable: provenance, SHA-256 and missingness documented; licence, authors, coordinates, deployment methods, calibration, quality control and funding/permits remain to be completed.\n\nSee [draft FAIR policy](FAIR_POLICY.md). This record is not fully FAIR-compliant.\n'
        (DIST/'metadata'/f'{filename}.meta.md').write_text(md)
    schema={'@context':'https://schema.org','@type':'Dataset','identifier':did,'name':title,'description':description,'url':ORIGIN+item['landing'],'version':'0.1.0-draft','keywords':fm['keywords'],'temporalCoverage':fm['temporal_start']+'/'+fm['temporal_end'],'variableMeasured':[{'@type':'PropertyValue','name':d['definition'],'unitText':d['unit']} for d in dictionary[2:]],'distribution':[{'@type':'DataDownload','name':r['source'],'encodingFormat':'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet','contentUrl':ORIGIN+'/files/'+r['source']},{'@type':'DataDownload','encodingFormat':'text/csv','contentUrl':ORIGIN+'/data/'+r['csv']}],'isAccessibleForFree':False}
    schema['spatialCoverage']={'@type':'Place','name':ICON_LOCATION['location'],'description':ICON_LOCATION['coordinate_basis'],'geo':{'@type':'GeoCoordinates','latitude':19.69960,'longitude':-80.06058}}
    schema['isBasedOn']=ICON_LOCATION['coordinate_source_url']
    item['schema']=schema
    (DIST/'metadata'/f'{did}.json').write_text(json.dumps(schema,indent=2,ensure_ascii=False))
    catalog.append(item)
shutil.copy2(ROOT/'ingest.py',DIST/'code/ingest.py')
(DIST/'code/requirements.txt').write_text('openpyxl>=3.1,<4\n')
code={'id':'ccmi-code-001','category':'code','title':'Logger export ingestion','description':'Reproducible Python importer for the seed workbooks. Checks SHA-256 equivalence, extracts timestamped rows to CSV and records observed temporal coverage and missingness.','variables':[],'format':['Python','JSON','CSV'],'status':'Draft code','start':None,'end':None,'depth':None,'coordinates':None,'location':None,'license':None,'creator':None,'contact':None,'doi':None,'version':'0.1.0-draft','records':None,'aliases':['ingest.py'],'metadata':'ingest.py.meta.md','landing':'/records/ccmi-code-001.html','notes':['Requires Python 3.10+ and openpyxl 3.1.x.','Outputs are extracted observations; no scientific quality control is performed.','Authorship and licence require approval before external reuse.'],'dictionary':[]}
code['sha256']=hashlib.sha256((DIST/'code/ingest.py').read_bytes()).hexdigest()
(DIST/'metadata/ingest.py.meta.md').write_text('---\nidentifier: "ccmi-code-001"\ncategory: "code"\nversion: "0.1.0-draft"\nlicense: null\ncreator: null\ncontact: null\nsha256: "'+code['sha256']+'"\n---\n\n# Logger export ingestion\n\n'+code['description']+'\n\n## Run\n\n```sh\npython -m pip install -r requirements.txt\npython ingest.py INPUT_DIRECTORY OUTPUT_DIRECTORY\n```\n\n## Provenance\n\nCreated for this repository on 2026-10-29. Inputs are original XLSX workbooks. Outputs: inventory.json and one CSV for each SHA-256-distinct workbook. Timestamp strings, headers, numeric values and missing cells are preserved for all rows with timestamps. Device metadata comes from the Details worksheet when present. No quality flags, averaging or conversion are introduced.\n\n## FAIR readiness\n\nStable local identifier, catalog record, documented requirements and SHA-256 supplied. Registered persistent identifier, steward contact, approved authorship, licence and long-term preservation remain pending. Related data: ccmi-env-001 through ccmi-env-006. See FAIR_POLICY.md.\n')
catalog.append(code)
from external_catalog import augment
catalog=augment(catalog,ROOT,DIST,ORIGIN)
from moorings import augment as add_moorings
catalog=add_moorings(catalog,ROOT,DIST,ORIGIN)
from hobo import augment as add_hobo
catalog=add_hobo(catalog,ROOT,DIST,ORIGIN)
from taxonomy import apply
apply(catalog,DIST)
from timeseries import build as build_timeseries
build_timeseries(catalog,DIST)
(DIST/'catalog.json').write_text(json.dumps(catalog,indent=2,ensure_ascii=False))
(DIST/'catalog-data.js').write_text('window.CATALOG = '+json.dumps(catalog,ensure_ascii=False)+';')
with zipfile.ZipFile(DIST/'metadata/ccmi-metadata.zip','w',zipfile.ZIP_DEFLATED) as z:
    for p in sorted((DIST/'metadata').rglob('*.md')): z.write(p,str(p.relative_to(DIST/'metadata')))
    for p in sorted((DIST/'metadata').rglob('*.json')): z.write(p,str(p.relative_to(DIST/'metadata')))
print(f'{len(catalog)} catalog records, {len(list((DIST/"metadata").rglob("*.meta.md")))} study/file metadata records')
template=(DIST/'index.html').read_text()
for d in catalog:
    page=re.sub(r'<title>.*?</title>','<title>'+d['title'].replace('&','&amp;')+' · CCMI Research Data</title>',template,count=1)
    if 'schema' in d:
        page=page.replace('</head>','<script type="application/ld+json">'+json.dumps(d['schema']).replace('</','<\\/')+'</script></head>')
    (DIST/'records'/f'{d["id"]}.html').write_text(page)
