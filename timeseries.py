"""Prepare finite logger observations for the browser; preserve missing values."""
import csv,json,math
from datetime import datetime, timezone, timedelta

def build(catalog,dist):
    series=[]
    for d in catalog:
        if not d['id'].startswith('ccmi-env-'):continue
        rows=[]
        with (dist/'data'/d['csv']).open() as f:
            reader=csv.reader(f);next(reader)
            for row in reader:
                t=int(datetime.fromisoformat(row[1]).replace(tzinfo=timezone(timedelta(hours=-5))).timestamp()*1000)
                def number(i):
                    if i>=len(row) or not row[i].strip():return None
                    v=float(row[i]);return v if math.isfinite(v) else None
                rows.append([t,number(2),number(3)])
        assert len(rows)==d['records']
        series.append({'id':d['id'],'title':d['title'],'depth':d['depth'],'depth_label':d.get('depth_label'),'site_id':d.get('site_id','icon'),'site_label':d.get('site_label','ICON nursery'),'location':{k:d.get(k) for k in ['latitude','longitude','location','coordinate_basis','coordinate_scope','location_status']},'timezone_interpretation':d.get('timezone_interpretation',d['timezone']),'csv':d['csv'],'csv_sha256':d['csv_sha256'],'landing':d['landing'],'metadata':d['metadata'],'interval_ms':d['interval']*60000,'has_light':'Light' in d['variables'],'rows':sorted(rows,key=lambda r:r[0])})
    (dist/'data/icon-timeseries.json').write_text(json.dumps({'timezone':'UTC-05:00','quality_control':'Not applied','series':series},separators=(',',':'),allow_nan=False))
