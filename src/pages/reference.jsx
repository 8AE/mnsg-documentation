import React, {useEffect, useMemo, useState} from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import {useHistory, useLocation} from '@docusaurus/router';
import api from '../data/api-index.json';

export default function Reference() {
  const location=useLocation();
  const history=useHistory();
  const [query,setQuery]=useState('');
  const [kind,setKind]=useState('');
  useEffect(()=>{const p=new URLSearchParams(location.search);setQuery(p.get('q')||'');setKind(['function','variable'].includes(p.get('kind'))?p.get('kind'):'');},[location.search]);
  const hits=useMemo(()=>{
    const q=query.toLowerCase().replace(/\\_/g,'_').trim();
    return api.filter(s=>(!kind||s.kind===kind)&&q.split(/\s+/).every(word=>`${s.name} ${s.title} ${s.summary} ${s.address||''} ${s.romAddress||''}`.toLowerCase().includes(word))).sort((a,b)=>{
      const rank=s=>q&&s.name.toLowerCase()===q?0:q&&s.name.toLowerCase().includes(q)?1:2;
      return rank(a)-rank(b)||a.name.localeCompare(b.name);
    });
  },[kind,query]);
  function update(q,k) {
    setQuery(q);setKind(k);
    const params=new URLSearchParams();if(q)params.set('q',q);if(k)params.set('kind',k);
    history.replace({pathname:location.pathname,search:params.size?'?'+params.toString():''});
  }
  return <Layout title="Symbol explorer" description="Search native Goemon functions and variables by name, address, or purpose."><main className="reference-container">
    <div className="home-eyebrow">API REFERENCE</div><h1>Symbol explorer</h1><p className="reference-lead">Find the interface. Understand the behavior.</p>
    <div className="reference-controls"><div className="reference-tabs" role="group" aria-label="Symbol type">{[['','All symbols'],['function','Functions'],['variable','Variables']].map(([value,label])=><button key={label} type="button" className={kind===value?'active':''} aria-pressed={kind===value} onClick={()=>update(query,value)}>{label}</button>)}</div><span className="reference-count" role="status">{hits.length} of {api.length} symbols</span></div>
    <div className="reference-input"><span aria-hidden="true">⌕</span><input type="search" value={query} onChange={e=>update(e.target.value,kind)} placeholder="Search by name, address, or purpose…" aria-label="Filter symbols"/></div>
    <div className="reference-table-wrap"><table className="reference-table"><thead><tr><th>Symbol / purpose</th><th>Type</th><th>Runtime address</th></tr></thead><tbody>{hits.map(s=><tr key={s.name}><td><Link to={s.url}><code>{s.name}</code><strong>{s.title}</strong></Link><p>{s.summary}</p></td><td><span className={`kind-badge ${s.kind}`}>{s.kind}</span></td><td><code>{s.address||'—'}</code></td></tr>)}</tbody></table></div>
    {!hits.length&&<div className="reference-empty"><h2>No matching symbols</h2><p>Try a partial name, an address, or a term like “room”.</p><button className="button button--secondary" onClick={()=>update('','')}>Clear filters</button></div>}
  </main></Layout>;
}
