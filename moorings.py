"""Catalog the user-supplied DoE January 2023 public mooring inventory."""
import json,csv,hashlib,shutil,re
import openpyxl
SOURCE_URL='https://doe.ky/resources/public-moorings/'
def augment(catalog,root,dist,origin):
    name='LITTLE-CAYMAN-PUBLIC-MOORINGS-2023.xlsx';src=root/'sources'/name
    w=openpyxl.load_workbook(src,data_only=True,read_only=True);s=w['Little Cayman']
    rows=list(s.values);headers=list(rows[0]);records=[dict(zip(headers,r)) for r in rows[1:] if r[0] is not None]
    assert len(records)==65 and len({r['ID'] for r in records})==65
    for r in records:
        assert 19.6<r['Northing']<19.8 and -80.2<r['Easting']<-79.9
        for key,decimal in [('Lat_DMmmm',r['Northing']),('Long_DMmmm',r['Easting'])]:
            nums=re.findall(r'[\d.]+',r[key]);value=float(nums[0])+float(nums[1])/60
            if 'W' in r[key]:value=-value
            assert abs(value-decimal)<1e-6
    shutil.copy2(src,dist/'files'/name)
    csvname='little-cayman-public-moorings-2023.csv'
    with (dist/'data'/csvname).open('w',newline='') as out:
        writer=csv.DictWriter(out,fieldnames=headers);writer.writeheader();writer.writerows(records)
    features=[{'type':'Feature','id':r['ID'],'geometry':{'type':'Point','coordinates':[r['Easting'],r['Northing']]},'properties':r} for r in records]
    geoname='little-cayman-public-moorings-2023.geojson'
    (dist/'data'/geoname).write_text(json.dumps({'type':'FeatureCollection','features':features},indent=2))
    points=[{'id':r['ID'],'name':r['Site_Name'],'coordinates':[r['Northing'],r['Easting']],'depth':r['Depth'],'pins':r['Pins'],'aspect':r['Aspect'],'mpa':r['MPA']} for r in records]
    note='DoE public mooring list, updated January 2023. Northing/Easting columns contain decimal latitude/longitude; coordinate strings cross-checked within 0.000001 degrees. Source datum not stated; WGS84 assumed for mapping. Depth retained in feet. MPA and mooring status are the source snapshot, not current operational guidance.'
    d={'id':'ccmi-reference-lc-moorings-2023','title':'Little Cayman public moorings — DoE 2023','category':'environmental','categories':['environmental'],'external':True,
       'description':'Public Department of Environment inventory of 65 Little Cayman mooring sites, with names, GPS coordinates, depth, pin count, aspect and source MPA designation.',
       'location':'Little Cayman, Cayman Islands','coordinates':None,'map_points':points,'variables':[],'format':['XLSX','CSV','GEOJSON'],'depth':None,'start':None,'end':None,'records':65,
       'status':'Public reference data · 2023 snapshot','metadata_checked':'2026-10-30','metadata_status':'Source fields checked; current mooring condition not verified',
       'version':'2023-01','paper_doi':None,'dataset_doi':None,'concept_doi':None,'doi':None,'paper_title':None,'paper_authors':[],'paper_year':None,'paper_relationship_status':'Reference inventory; no associated paper',
       'dataset_creators':['Cayman Islands Department of Environment'],'dataset_title':'Little Cayman Public Moorings 2023','license':None,'license_url':None,
       'repository_url':SOURCE_URL,'repository_accession':None,'source_repositories':[{'provider':'Cayman Islands DoE','url':SOURCE_URL,'version':'January 2023'}],
       'notes':[note,'Original XLSX supplied by the user and attributed to the public DoE list. CSV and GeoJSON are derived without changing source values. GeoJSON uses longitude/latitude order; the map uses latitude/longitude.','Public availability is documented; no explicit reuse licence was assigned.','Mooring positions are reference infrastructure points, not inferred locations for ecological observations.'],
       'metadata':'ccmi-reference-lc-moorings-2023.meta.md','landing':'/records/ccmi-reference-lc-moorings-2023.html','files':[]}
    for filename,folder in [(name,'files'),(csvname,'data'),(geoname,'data')]:
        path=dist/folder/filename;url=origin+'/'+folder+'/'+filename
        ident='ccmi-file-'+hashlib.sha256((d['id']+'\n'+url).encode()).hexdigest()[:16]
        f={'id':ident,'parent_id':d['id'],'title':filename,'name':filename,'url':url,'repository_url':SOURCE_URL,'provider':'Cayman Islands DoE' if folder=='files' else 'CCMI · derived from DoE',
           'version':'2023-01','kind':'data','category':'environmental','format':path.suffix[1:].upper(),'size_bytes':path.stat().st_size,'checksum':hashlib.sha256(path.read_bytes()).hexdigest(),'checksum_type':'sha256',
           'source_license':None,'paper_doi':None,'dataset_doi':None,'concept_doi':None,'doi_scope':'No DOI assigned; cite the DoE January 2023 inventory.',
           'landing':'/?file='+ident,'metadata':'file-records/'+ident+'.meta.md','metadata_json':'file-records/'+ident+'.json','metadata_checked':'2026-10-30',
           'link_status':'Original file retained; coordinates cross-checked against source degree-minute strings.','external':False,'location':d['location'],'map_points':points,'coordinate_basis':note}
        d['files'].append(f)
        (dist/'metadata'/f['metadata_json']).write_text(json.dumps(f,indent=2))
        (dist/'metadata'/f['metadata']).write_text('---\n'+'\n'.join(k+': '+json.dumps(v) for k,v in f.items() if k!='map_points')+'\n---\n\n# '+filename+'\n\n'+note+'\n\n[DoE source page]('+SOURCE_URL+'). No explicit reuse licence recorded.\n')
    d['aliases']=[f['name'] for f in d['files']]
    d['schema']={'@context':'https://schema.org','@type':'Dataset','identifier':d['id'],'name':d['title'],'description':d['description'],'creator':{'@type':'GovernmentOrganization','name':d['dataset_creators'][0]},'version':'2023-01','url':origin+d['landing'],'isBasedOn':SOURCE_URL,'spatialCoverage':{'@type':'Place','name':d['location'],'geo':{'@type':'GeoShape','box':f"{min(r['Northing'] for r in records)} {min(r['Easting'] for r in records)} {max(r['Northing'] for r in records)} {max(r['Easting'] for r in records)}"}},'distribution':[{'@type':'DataDownload','contentUrl':f['url'],'encodingFormat':f['format']} for f in d['files']]}
    (dist/'metadata'/(d['id']+'.json')).write_text(json.dumps(d['schema'],indent=2))
    (dist/'metadata'/d['metadata']).write_text('---\n'+ '\n'.join(k+': '+json.dumps(v) for k,v in d.items() if k not in ['files','map_points','schema'])+'\n---\n\n# '+d['title']+'\n\n'+d['description']+'\n\n## Provenance\n\n'+'\n\n'.join(d['notes'])+'\n\n[DoE source page]('+SOURCE_URL+').\n')
    (dist/'moorings-data.js').write_text('window.MOORINGS = '+json.dumps({'record_id':d['id'],'landing':d['landing'],'points':points})+';')
    catalog.append(d);return catalog
