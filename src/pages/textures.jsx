import React, {useEffect, useMemo, useState} from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import {useHistory, useLocation} from '@docusaurus/router';
import catalog from '../data/textures.json';

function TextureImage({image, label, className = ''}) {
  return <img className={`native-texture ${className}`} src={useBaseUrl(image)} alt={label} loading="lazy" />;
}

export default function Textures() {
  const [query, setQuery] = useState('');
  const [showAll, setShowAll] = useState(false);
  const location = useLocation();
  const history = useHistory();
  useEffect(() => { setQuery(new URLSearchParams(location.search).get('q') || ''); }, [location.search]);
  function updateQuery(value) {
    setQuery(value);
    history.replace({pathname: location.pathname, search: value ? `?q=${encodeURIComponent(value)}` : ''});
  }
  const hits = useMemo(() => {
    const words = query.toLowerCase().trim().split(/\s+/);
    return catalog.resources.filter(row => (showAll || row.identified || query.trim()) && words.every(word =>
      `${row.id} ${row.romAddress} ${row.label} ${row.nativeHandle || ''} ${row.symbols.join(' ')}`.toLowerCase().includes(word)));
  }, [query, showAll]);
  return <Layout title="Native texture gallery" description="Original game textures indexed by ROM resource, address, and native variable.">
    <main className="reference-container texture-gallery">
      <div className="home-eyebrow">NATIVE ASSETS · US ROM</div>
      <h1>Texture gallery</h1>
      <p className="reference-lead">Original game textures, with the addresses that identify them.</p>
      <p>Browse {catalog.icons.length} verified item and character crops and {catalog.resources.length} decoded sheets.
        Each sheet is shown in stored pixel order; crops reproduce its displayed orientation.
        Resources are ROM assets, while texture handles are runtime storage in the named overlay.</p>
      <p>Load these assets with <Link to="/functions/func_800144E8_150E8/">the native resource decoder</Link>.
        Matched <code>D_…</code> names are the exact texture-handle variables from the recomp symbol table.
        Resources without a verified variable keep their ROM address.</p>
      <label className="texture-search">Find a texture
        <input type="search" value={query} onChange={e => updateQuery(e.target.value)} placeholder="Flute, 0x8016, 0x007EB740, D_80217FAC_676F5C…" />
      </label>
      <label className="texture-toggle"><input type="checkbox" checked={showAll} onChange={e => setShowAll(e.target.checked)} /> Include all inspected sheets, including those whose purpose is unidentified</label>
      <p role="status">{hits.length} matching sheets</p>
      <div className="texture-grid">
        {hits.map(row => <article className="texture-card" id={`resource-${row.id.toLowerCase()}`} key={row.id}>
          <h2>{row.nativeSymbol ? <Link to={`/variables/${row.nativeSymbol}/#native-textures`}><code>{row.nativeSymbol}</code></Link> : <a href={`#resource-${row.id.toLowerCase()}`}>{row.id}</a>}</h2>
          <p>{row.label}</p>
          <TextureImage image={row.image} label={`${row.id} original ${row.width} by ${row.height} sheet`} className="texture-sheet" />
          <dl><dt>Resource ID</dt><dd><code>{row.id}</code></dd>
            <dt>Packed image ROM address</dt><dd><code>{row.romAddress}</code></dd>
            <dt>Stored / decoded</dt><dd>{row.packedSize} / {row.width * row.height * 2} bytes · {row.width} × {row.height}</dd>
            {row.nativeHandle && <><dt>Texture handle storage</dt><dd><code>{row.nativeHandle}</code> · <code>{row.nativeOverlay}</code></dd></>}
            {row.segmentedAddress && <><dt>Segmented texture address</dt><dd><code>{row.segmentedAddress}</code></dd></>}
          </dl>
          {row.addressNote && <p>{row.addressNote}</p>}
          {catalog.icons.filter(icon => icon.resource === row.id).map(icon => <div className="texture-crop" key={icon.name}>
            <TextureImage image={icon.image} label={icon.label} />
            <div><strong>{icon.label}</strong><div>Crop ({icon.x}, {icon.y}, {icon.width}, {icon.height}){icon.flipY ? ' · flip vertically' : ''}</div>
              {icon.symbols.map(symbol => <Link key={symbol} to={`/variables/${symbol}/#native-textures`}><code>{symbol}</code></Link>)}
            </div>
          </div>)}
        </article>)}
      </div>
      {!hits.length && <p>No textures match. Try a resource ID, ROM address, native handle, or item name.</p>}
    </main>
  </Layout>;
}
