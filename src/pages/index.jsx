import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import api from '../data/api-index.json';

const features = [
  {name:'func_800240DC_24CDC',title:'Read a game flag',type:'functions',icon:'ƒ',description:'Query progression and encounter state.'},
  {name:'D_800C7AB2',title:'Get the current room',type:'variables',icon:'◈',description:'Understand room identity and transitions.'},
  {name:'func_80002040_2C40',title:'Observe the system update',type:'functions',icon:'↪',description:'Work with the native system-step dispatcher.'},
];

export default function Home() {
  const functionCount=api.filter(s=>s.kind==='function').length;
  return <Layout title="Native API reference" description="Explore Mystical Ninja Starring Goemon's native functions and variables, with C interfaces and practical usage examples.">
    <main className="home-container">
      <div className="home-eyebrow">MYSTICAL NINJA STARRING GOEMON <span>US RECOMPILATION</span></div>
      <section className="home-hero">
        <div><h1>Know the game.<br/><span>Build on it.</span></h1><p>A practical reference to Goemon’s native API.<br/>Understand the functions, read the state, and write the C.</p><div className="hero-actions"><Link className="button button--primary button--lg" to="/reference">Explore the API <span aria-hidden="true">→</span></Link><Link className="home-secondary" to="/getting-started">Getting started ↗</Link></div></div>
        <div className="home-art" aria-hidden="true"><div className="art-ring"/><div className="art-ring second"/><div className="art-symbol">{'{'}<span>忍</span>{'}'}</div><span className="art-address">0x80000400 · MIPS</span></div>
      </section>
      <div className="home-stats"><div><strong>{api.length}</strong><span>documented symbols</span></div><div><strong>{functionCount}</strong><span>native functions</span></div><div><strong>{api.length-functionCount}</strong><span>external variables</span></div><div><strong>C</strong><span>practical examples</span></div></div>
      <div className="home-section-heading"><h2>A place to start</h2><span>From address to understanding</span></div>
      <section className="home-feature-grid" aria-label="Featured API pages">{features.map(s=><Link key={s.name} className="home-feature" to={`/${s.type}/${s.name}`}><span className="feature-type">{s.icon}</span><span className="feature-arrow" aria-hidden="true">↗</span><h3>{s.title}</h3><code>{s.name}</code><p>{s.description}</p></Link>)}</section>
      <section className="home-bottom"><div><span className="home-eyebrow">THE NATIVE INTERFACE</span><h2>A reference you can work with.</h2><p>Look up a symbol by name, address, or purpose. Each page explains its interface, behavior, and requirements, with C examples ready to adapt.</p></div><div className="home-topics"><Link to="/functions"><span>01</span><div><h3>Functions</h3><p>Calls, callbacks, parameters, and return values.</p></div><span>→</span></Link><Link to="/variables"><span>02</span><div><h3>Variables</h3><p>Game state, memory layout, and typed access.</p></div><span>→</span></Link><Link to="/native-lifecycle"><span>03</span><div><h3>Native lifecycle</h3><p>Room transitions, actors, and loaded resources.</p></div><span>→</span></Link></div></section>
    </main>
  </Layout>;
}
