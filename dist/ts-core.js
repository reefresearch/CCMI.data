(()=>{'use strict';
const offset=5*3600000;
function aggregate(rows,column,resolution){
 if(resolution==='native')return rows.map(r=>({t:r[0],v:r[column],min:r[column],max:r[column],n:r[column]===null?0:1,total:1}));
 const width=resolution==='hourly'?3600000:86400000,buckets=new Map();
 for(const r of rows){const t=Math.floor((r[0]-offset)/width)*width+offset;let b=buckets.get(t);if(!b){b={t,v:null,min:null,max:null,n:0,total:0,sum:0};buckets.set(t,b);}b.total++;if(r[column]!==null){const v=r[column];b.sum+=v;b.n++;b.min=b.min===null?v:Math.min(b.min,v);b.max=b.max===null?v:Math.max(b.max,v);}}
 return [...buckets.values()].map(b=>({...b,v:b.n?b.sum/b.n:null}));
}
function nearest(points,t){let lo=0,hi=points.length;while(lo<hi){const m=(lo+hi)>>1;if(points[m].t<t)lo=m+1;else hi=m;}if(!lo)return points[0];if(lo===points.length)return points[lo-1];return t-points[lo-1].t<points[lo].t-t?points[lo-1]:points[lo];}
function csv(series,{parameter,resolution,native=false}){
 const quote=v=>'"'+String(v??'').replace(/"/g,'""')+'"',stamp=t=>new Date(t-offset).toISOString().slice(0,19).replace('T',' ');
 const lines=[['series_id','source_csv','timestamp_utc_minus_05','parameter','unit','resolution','value','minimum','maximum','valid_count','source_row_count','quality_control'].map(quote).join(',')];
 for(const s of series){const points=native?aggregate(s.selectedRows,parameter==='light'?2:1,'native'):s.points;for(const p of points)lines.push([s.id,s.csv,stamp(p.t)+'-05:00',parameter,parameter==='light'?'lux':'degC',native?'native':resolution,p.v,p.min,p.max,p.n,p.total,'not applied'].map(quote).join(','));}
 return lines.join('\r\n');
}
window.TSCore={aggregate,nearest,offset,csv};
})();
