import React, {useEffect, useMemo, useRef, useState} from 'react';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import api from '@site/src/data/api-index.json';

const normalize = value => value.toLowerCase().replace(/\\_/g, '_').trim();
export default function SearchBar() {
  const [query, setQuery] = useState('');
  const [open, setOpen] = useState(false);
  const input = useRef(null);
  const container = useRef(null);
  const resultLinks = useRef([]);
  const referenceUrl = useBaseUrl('/reference/');
  const hits = useMemo(() => {
    const q = normalize(query);
    if (!q) return [];
    return api.filter(s => q.split(/\s+/).every(word => normalize(`${s.name} ${s.title} ${s.summary} ${s.address || ''} ${s.romAddress || ''} ${s.values || ''} ${s.textures || ''}`).includes(word)))
      .sort((a, b) => {
        const rank = s => normalize(s.name) === q ? 0 : normalize(s.name).includes(q) ? 1 : 2;
        return rank(a) - rank(b) || a.name.localeCompare(b.name);
      }).slice(0, 7);
  }, [query]);
  useEffect(() => {
    const keyboard = e => {
      if ((e.key === '/' && !/INPUT|TEXTAREA|SELECT/.test(document.activeElement?.tagName)) || (e.key === 'k' && (e.metaKey || e.ctrlKey))) {
        e.preventDefault(); input.current?.focus(); setOpen(true);
      }
      if (e.key === 'Escape') {
        if (container.current?.contains(e.target)) input.current?.focus();
        setOpen(false);
      }
    };
    const outside = e => { if (!container.current?.contains(e.target)) setOpen(false); };
    document.addEventListener('keydown', keyboard);
    document.addEventListener('pointerdown', outside);
    return () => { document.removeEventListener('keydown', keyboard); document.removeEventListener('pointerdown', outside); };
  }, []);
  function dismiss() { setOpen(false); setQuery(''); }
  return <div className="native-search" ref={container}>
    <form action={referenceUrl} role="search">
      <span className="search-glyph" aria-hidden="true">⌕</span>
      <input ref={input} type="search" name="q" value={query} placeholder="Search the API…" aria-label="Search functions and variables" aria-describedby="native-search-status" aria-controls={open && query.trim() ? 'native-search-results' : undefined} autoComplete="off" onFocus={() => setOpen(true)} onChange={e => {setQuery(e.target.value); setOpen(true);}}
        onKeyDown={e => {if (e.key === 'ArrowDown' && hits.length) {e.preventDefault(); resultLinks.current[0]?.focus();}}} />
      <kbd>/</kbd>
    </form>
    <span id="native-search-status" className="native-search-status" role="status">{open && query.trim() ? `${hits.length} search suggestions. Use the down arrow to explore results.` : ''}</span>
    {open && query.trim() && <div id="native-search-results" className="native-search-results" role="region" aria-label="Search suggestions">
      {hits.map((s, i) => <Link key={s.name} to={s.url} ref={el => {resultLinks.current[i] = el;}} onClick={dismiss} onKeyDown={e => {
        if (e.key === 'ArrowDown') {e.preventDefault(); resultLinks.current[Math.min(i+1,hits.length-1)]?.focus();}
        if (e.key === 'ArrowUp') {e.preventDefault(); (i ? resultLinks.current[i-1] : input.current)?.focus();}
      }}><span className={`symbol-kind ${s.kind}`}>{s.kind === 'function' ? 'ƒ' : '◈'}</span><span><code>{s.name}</code><small>{s.title}</small></span><span aria-hidden="true">↗</span></Link>)}
      {!hits.length && <p>No matching symbols. Try a partial address or a term like “room”.</p>}
      <Link className="all-results" to={`/reference/?q=${encodeURIComponent(query)}`} onClick={dismiss}>View all results →</Link>
    </div>}
  </div>;
}
