"""Versioned CCMI browsing subjects; source categories remain for legacy URLs."""
import json
SUBJECTS=[
 ('environmental-conditions','Environmental conditions','Temperature, light and heat-stress observations.'),
 ('biodiversity-communities','Biodiversity & communities','Species abundance, benthic composition and recruitment.'),
 ('physiology-performance','Physiology & performance','Growth, photosynthesis, respiration and thermal performance.'),
 ('microbiology-molecular','Microbiology & molecular data','Microbiomes, molecular tables and sequence reads.'),
 ('coral-health-restoration','Coral health & restoration','Bleaching, disease, nurseries and outplanting.'),
 ('human-pressures-management','Human pressures & management','Human activity, protection status and management comparisons.')]
E,B,P,M,H,U=[s[0] for s in SUBJECTS]
STUDIES={
 'endozoicomonas':[M,U], 'nursery-microbiomes':[M,H], 'outplanting':[P,H],
 'nursery-heatwave':[E,H], 'mesophotic-refuge':[E,H], 'bleaching-2023':[E,H],
 'madracis':[P,M], 'photoacclimation':[E,B,P], 'genotype-disease':[H],
 'seagrass':[P], 'pickle-bank':[B], 'quiet-oceans':[B,U],
 'agrra-1999-2023':[B], 'whiteband':[M,H]}

def apply(catalog,dist):
    meta=dist/'metadata'
    labels=dict((s[0],s[1]) for s in SUBJECTS)
    vocabulary={'id':'ccmi-subjects','version':'1.0.0','status':'CCMI browsing vocabulary; steward review pending',
        'note':'Locally defined subjects, not asserted GCMD equivalents. Subjects may overlap. File assignments use repository context and filename rules; code and documentation inherit study subjects. No scientific content audit is implied.',
        'subjects':[{'id':i,'label':l,'definition':d} for i,l,d in SUBJECTS]}
    (meta/'subjects.json').write_text(json.dumps(vocabulary,indent=2))
    (dist/'taxonomy-data.js').write_text('window.SUBJECTS = '+json.dumps(vocabulary['subjects'])+';')
    def fields(obj):return {k:obj[k] for k in ['subjects','subject_labels','subject_basis','subject_vocabulary','resource_types']}
    def enrich(obj,subjects,basis,types):
        obj.update(subjects=subjects,subject_labels=[labels[s] for s in subjects],subject_basis=basis,
                   subject_vocabulary='ccmi-subjects:1.0.0',resource_types=sorted(set(types)))
    def md_update(path,obj):
        if path.exists():
            text=path.read_text(); head,body=text[4:].split('\n---',1)
            additions='\n'.join(k+': '+json.dumps(v) for k,v in fields(obj).items())
            path.write_text('---\n'+head+'\n'+additions+'\n---'+body)
    allfiles=[]
    for d in catalog:
        topics=[U] if d['id']=='ccmi-reference-lc-moorings-2023' else STUDIES.get(d['id'].removeprefix('ccmi-study-'),[E])
        types=['code' if f['kind']=='code' else 'documentation' if f['kind']=='documentation' else 'data' for f in d['files']]
        enrich(d,topics,'Curated from catalog study description; steward review pending.',types)
        for f in d['files']:
            if d['id']=='ccmi-reference-lc-moorings-2023':topics_f=[U]
            elif f['kind']=='sequence': topics_f=[M]
            elif f['category']=='environmental' and f['kind']=='data':topics_f=[E]
            elif f['kind']=='data':topics_f=[s for s in topics if s!=E] or topics
            else:topics_f=topics
            enrich(f,topics_f,'Filename and repository context; code, documentation and archives inherit study subjects. Steward review pending.',
                   ['code' if f['kind']=='code' else 'documentation' if f['kind']=='documentation' else 'data'])
            path=meta/f['metadata_json']; obj=json.loads(path.read_text());obj.update(fields(f));path.write_text(json.dumps(obj,indent=2,ensure_ascii=False))
            md_update(meta/f['metadata'],f);allfiles.append(f)
        md_update(meta/d['metadata'],d)
        for alias in d.get('aliases',[]):
            p=meta/(alias+'.meta.md')
            if p.exists() and p!=meta/d['metadata']:md_update(p,d)
        schema_path=meta/(d['id']+'.json')
        schema=json.loads(schema_path.read_text()) if schema_path.exists() else d.get('schema')
        if schema:
            schema['keywords']=list(dict.fromkeys(schema.get('keywords',[])+d['subject_labels']))
            schema['about']=[{'@type':'DefinedTerm','termCode':s,'name':labels[s],'inDefinedTermSet':'ccmi-subjects:1.0.0'} for s in topics]
            schema_path.write_text(json.dumps(schema,indent=2,ensure_ascii=False));d['schema']=schema
    (dist/'file-catalog.json').write_text(json.dumps(allfiles,indent=2,ensure_ascii=False))
