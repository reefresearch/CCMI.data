"""Import user-supplied MF HOBO CSVs; retain originals and label location inference."""
import csv, hashlib, json, shutil
from collections import Counter
from datetime import datetime
from urllib.parse import quote

EVIDENCE='https://www.ncbi.nlm.nih.gov/biosample/SAMN55782138'
DOE='https://doe.ky/resources/public-moorings/'
CHECKED='2026-10-30'

def sha(path):return hashlib.sha256(path.read_bytes()).hexdigest()
def markdown(path, obj, text):
    path.write_text('---\n'+'\n'.join(k+': '+json.dumps(v,ensure_ascii=False) for k,v in obj.items())+'\n---\n\n'+text)

def augment(catalog,root,dist,origin):
    moorings=list(csv.DictReader((dist/'data/little-cayman-public-moorings-2023.csv').open()))
    mooring=next(r for r in moorings if r['Site_Name']=="Martha's Finyard")
    coords=[float(mooring['Northing']),float(mooring['Easting'])]
    basis="Probable identification: MF = Martha's Finyard. NCBI BioSample SAMN55782138 uses MF in its sample name, explicitly names Martha's Finyard, and reports 19.66487 N, 80.11118 W. These agree with the supplied DoE January 2023 mooring 237 coordinates. This supports an abbreviation match, not confirmation of the 2016 deployment or logger positions."
    spatial={'coordinates':coords,'latitude':coords[0],'longitude':coords[1],
       'location':"Martha's Finyard, Little Cayman — probable MF site reference",
       'coordinate_basis':basis,'coordinate_source':'Cayman Islands DoE public moorings, January 2023, ID 237; abbreviation corroborated by NCBI BioSample SAMN55782138 (2023 samples).',
       'coordinate_source_url':EVIDENCE,'coordinate_sources':[DOE,EVIDENCE],
       'coordinate_scope':'tentative site / mooring reference; not a verified logger position',
       'coordinate_datum':'WGS84 assumed for mapping; source datum not specified','coordinate_uncertainty_m':None,
       'location_status':'inferred; steward confirmation required'}
    evidence={'checked':CHECKED,'candidate_site':mooring,'abbreviation_evidence':{'url':EVIDENCE,'sample_name':'117-MF-SD-44','site':"Martha's Finyard",'collection_date':'2023-07','latitude':19.66487,'longitude':-80.11118},'interpretation':basis}
    (root/'sources/hobo-location-evidence.json').write_text(json.dumps(evidence,indent=2))
    for number,label in [(7,'Deep'),(8,'Mid')]:
        name=f'161005_CCMI_HOBO_MF_{label} October 2016.csv'
        source=root/'sources/hobo'/name
        aliases=[name,name.replace('.csv','(1).csv')]
        assert all(sha(root/'sources/hobo'/a)==sha(source) for a in aliases)
        with source.open(newline='',encoding='utf-8-sig') as handle:
            reader=csv.DictReader(handle);headers=reader.fieldnames;rows=list(reader)
        assert rows and len({r['timestamp'] for r in rows})==len(rows)
        dates=[datetime.fromisoformat(r['timestamp']) for r in rows]
        assert all(b>a for a,b in zip(dates,dates[1:]))
        interval=Counter((b-a).total_seconds()/60 for a,b in zip(dates,dates[1:])).most_common(1)[0][0]
        assert {r['timezone_label'] for r in rows}=={'Central Daylight Time'}
        values=[float(r['temperature_c']) for r in rows if r['temperature_c'].strip()]
        did=f'ccmi-env-{number:03d}';csvname=f'HOBO_MF_{label}_2016.csv'
        with (dist/'data'/csvname).open('w',newline='') as handle:
            writer=csv.writer(handle);writer.writerow(['sample_index','timestamp','temperature_c'])
            writer.writerows([i,r['timestamp'],r['temperature_c']] for i,r in enumerate(rows,1))
        notes=[basis,'Deep / Mid and MF-BOT-46 / MF-MID-47 are source labels. Numeric water depths and the meanings of 46 / 47 are not established.',
          'Source timezone_label is Central Daylight Time, interpreted as fixed UTC−05:00 for this June–October export. Logger clock settings are unverified; original timestamp strings are retained.',
          'Date-only source timestamp strings are interpreted as 00:00:00 on that date; original strings are retained.',
          'Temperature values are used as supplied. raw_temperature is retained in the originals; its units and conversion/calibration history are not established.',
          'No quality-control exclusions, calibration corrections or deployment-window screening applied. Observation coverage is not a verified in-water period.',
          'Two uploads per series have identical SHA-256 hashes. All originals are retained; only one canonical original and one normalized CSV are indexed per series.']
        dictionary=[{'column':h,'definition':{'timestamp':'Observation timestamp (source wall time)','temperature_c':'Temperature, supplied in degrees Celsius','raw_temperature':'Raw source value; units and conversion unverified','supported_model':'Source model label','serial_number':'Logger serial number','deployment_description':'Source deployment label','logging_interval_seconds':'Source logging interval in seconds','timezone_label':'Source timezone label'}[h],
           'unit':'°C' if h=='temperature_c' else 's' if h=='logging_interval_seconds' else None,
           'missing':sum(not r[h].strip() for r in rows),'valid_count':sum(bool(r[h].strip()) for r in rows)} for h in headers]
        d={'id':did,'hobo':True,'external':True,'category':'environmental','categories':['environmental'],
          'title':f'MF HOBO {label} — temperature · Jun–Oct 2016',
          'description':f"HOBO temperature observations labelled {rows[0]['deployment_description']}: {len(rows):,} timestamped records from {rows[0]['timestamp'][:10]} to {rows[-1]['timestamp'][:10]}, at a modal {interval:g}-minute interval. MF probably refers to Martha's Finyard; the mapped position is a tentative site reference. {label} is a source depth label; depth in metres is unknown.",
          'depth':None,'depth_label':label,'depth_basis':'qualitative source label; numeric depth not established','variables':['Temperature'],
          'site_id':'mf','site_label':"MF · probably Martha's Finyard",'start':rows[0]['timestamp'],'end':rows[-1]['timestamp'],
          'records':len(rows),'interval':interval,'timezone':'Central Daylight Time (source label); interpreted UTC−05:00',
          'timezone_interpretation':'UTC−05:00 assumed from source CDT label for June–October 2016; clock configuration unverified',
          'format':['CSV'],'status':'Location inferred · review pending','license':None,'creator':None,'contact':None,
          'paper_doi':None,'dataset_doi':None,'concept_doi':None,'doi':None,'paper_title':None,'paper_year':None,
          'paper_authors':[],'dataset_creators':[],'paper_relationship_status':'No paper association established for these uploads.',
          'repository_accession':None,'repository_url':origin+'/?page=explorer&site=mf','source_repositories':[{'provider':'CCMI · supplied HOBO exports','url':origin+'/?content=files&study='+did,'version':CHECKED}],
          'version':'0.1.0-draft','metadata_checked':CHECKED,'instrument':rows[0]['supported_model'],'serial':rows[0]['serial_number'],
          'deployment_description':rows[0]['deployment_description'],'dictionary':dictionary,'notes':notes,'aliases':aliases,
          'sha256':sha(source),'bytes':source.stat().st_size,'csv':csvname,'csv_sha256':sha(dist/'data'/csvname),
          'metadata':did+'.meta.md','landing':'/records/'+did+'.html','files':[],
          'temperature_summary':{'valid':len(values),'missing':len(rows)-len(values),'minimum':min(values),'maximum':max(values)},**spatial}
        for alias in aliases:
            shutil.copy2(root/'sources/hobo'/alias,dist/'files'/alias)
            markdown(dist/'metadata'/(alias+'.meta.md'),{k:v for k,v in d.items() if k not in ['files','dictionary']},'# '+d['title']+'\n\nOriginal source file: '+alias+'\n\n'+ '\n\n'.join(notes))
        for filename,folder in [(name,'files'),(csvname,'data')]:
            path=dist/folder/filename;url=origin+'/'+folder+'/'+quote(filename)
            fid='ccmi-file-'+hashlib.sha256((did+'\n'+url).encode()).hexdigest()[:16]
            f={'id':fid,'parent_id':did,'title':filename,'name':filename,'url':url,'repository_url':origin+d['landing'],
              'provider':'CCMI · HOBO export' if folder=='files' else 'CCMI · normalized observations','version':d['version'],
              'kind':'data','category':'environmental','format':'CSV','size_bytes':path.stat().st_size,'checksum':sha(path),'checksum_type':'sha256',
              'source_license':None,'paper_doi':None,'dataset_doi':None,'concept_doi':None,'doi_scope':'No paper or dataset DOI established for this source.',
              'landing':'/?file='+fid,'metadata':'file-records/'+fid+'.meta.md','metadata_json':'file-records/'+fid+'.json',
              'metadata_checked':CHECKED,'link_status':'Hosted file; checksum verified against supplied source or generated normalization. Scientific QC not applied.',
              'external':False,'variables':['Temperature'],'depth':None,'depth_label':label,'start':d['start'],'end':d['end'],
              'timezone':d['timezone'],'instrument':d['instrument'],'serial':d['serial'],'deployment_description':d['deployment_description'],**spatial}
            d['files'].append(f)
            (dist/'metadata'/f['metadata_json']).write_text(json.dumps(f,indent=2))
            markdown(dist/'metadata'/f['metadata'],f,'# '+filename+'\n\n'+ '\n\n'.join(notes)+'\n\nNormalization adds a sequential sample index and selects timestamp and temperature_c without rounding or changing timestamp strings. Full source metadata and raw_temperature remain in the original CSV.')
        schema={'@context':'https://schema.org','@type':'Dataset','identifier':did,'name':d['title'],'description':d['description'],
          'url':origin+d['landing'],'version':d['version'],'temporalCoverage':d['start'].replace(' ','T')+'-05:00/'+d['end'].replace(' ','T')+'-05:00',
          'variableMeasured':[{'@type':'PropertyValue','name':'Temperature','unitText':'°C'}],
          'spatialCoverage':{'@type':'Place','name':d['location'],'description':basis,'geo':{'@type':'GeoCoordinates','latitude':coords[0],'longitude':coords[1]}},
          'isBasedOn':[DOE,EVIDENCE],'distribution':[{'@type':'DataDownload','name':f['name'],'encodingFormat':'text/csv','contentUrl':f['url']} for f in d['files']],
          'isAccessibleForFree':False}
        d['schema']=schema
        (dist/'metadata'/(did+'.json')).write_text(json.dumps(schema,indent=2))
        body='# '+d['title']+'\n\n'+d['description']+'\n\n## Provenance and location inference\n\n'+'\n\n'.join(notes)+'\n\nLocation evidence: ['+EVIDENCE+']('+EVIDENCE+'); DoE January 2023 inventory, mooring 237.\n\n## Data dictionary\n\n| Column | Definition | Units | Valid | Missing |\n| --- | --- | --- | ---: | ---: |\n'
        body+='\n'.join(f"| {v['column']} | {v['definition']} | {v['unit'] or 'not specified / not applicable'} | {v['valid_count']} | {v['missing']} |" for v in dictionary)
        body+='\n\n## FAIR preparation\n\nFindable: local identifiers and searchable metadata; DOI not registered. Accessible: original and normalized CSVs on this site, subject to site access. Interoperable: documented units, source labels and timezone interpretation; machine-readable JSON-LD. Reusable: SHA-256, original metadata, provenance and provisional location supplied; authorship, reuse licence, deployment depths, clock configuration, collection methods and QC await confirmation. No open reuse licence is implied.\n'
        markdown(dist/'metadata'/d['metadata'],{k:v for k,v in d.items() if k not in ['files','schema','dictionary']},body)
        catalog.append(d)
    return catalog
