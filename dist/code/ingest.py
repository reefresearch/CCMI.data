"""Inspect original logger exports without changing their contents.

Usage: python ingest.py INPUT_DIRECTORY OUTPUT_DIRECTORY
Requires Python >=3.10 and openpyxl >=3.1,<4.
SHA-256 groups byte-identical inputs. CSV preserves all timestamped rows,
including missing measurements and original timestamp strings. No QC is applied.
"""
from pathlib import Path
from datetime import datetime
from collections import Counter
import csv, hashlib, json, sys
import openpyxl

def ingest(input_dir, output_dir):
    output_dir=Path(output_dir); output_dir.mkdir(parents=True,exist_ok=True)
    groups={}
    for path in sorted(Path(input_dir).glob('*.xlsx')):
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        if digest in groups:
            groups[digest]['aliases'].append(path.name)
            continue
        workbook=openpyxl.load_workbook(path,read_only=True,data_only=True)
        sheet=workbook.worksheets[0]; rows=iter(sheet.values)
        for header in rows:
            if len(header)>1 and header[1] and 'Date' in str(header[1]): break
        else: raise ValueError(f'No timestamp header: {path.name}')
        data=[row for row in rows if len(row)>1 and row[1] is not None]
        timestamps=[str(row[1]) for row in data]
        parsed=[datetime.fromisoformat(t) for t in timestamps]
        deltas=Counter((b-a).total_seconds()/60 for a,b in zip(parsed,parsed[1:]))
        details={str(r[2]):str(r[3]) for sh in workbook if sh.title=='Details' for r in sh.values if len(r)>3 and r[2] and r[3] is not None}
        target=output_dir/f'{path.stem}.csv'
        with target.open('w',newline='') as stream:
            writer=csv.writer(stream); writer.writerow(header); writer.writerows(data)
        record={'source':path.name,'aliases':[path.name],'sha256':digest,'bytes':path.stat().st_size,'sheet':sheet.title,'sheets':workbook.sheetnames,'headers':list(header),'records':len(data),'start':min(timestamps),'end':max(timestamps),'timestamp_label':str(header[1]),'timezone':'UTC-05:00 as labelled; not converted','interval_minutes':deltas.most_common(1)[0][0] if deltas else None,'interval_counts':dict(deltas),'duplicate_timestamps':len(timestamps)-len(set(timestamps)),'non_monotonic_steps':sum(v for k,v in deltas.items() if k<=0),'missing':[sum(len(r)<=i or r[i] is None for r in data) for i in range(len(header))],'details':details,'csv':target.name,'csv_sha256':hashlib.sha256(target.read_bytes()).hexdigest()}
        groups[digest]=record
        workbook.close()
    records=list(groups.values())
    (output_dir/'inventory.json').write_text(json.dumps(records,indent=2))
    return records

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('Usage: python ingest.py INPUT_DIRECTORY OUTPUT_DIRECTORY')
    result=ingest(sys.argv[1],sys.argv[2]); print(f'{len(result)} unique workbooks inspected')
