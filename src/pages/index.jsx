import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';
import useBaseUrl from '@docusaurus/useBaseUrl';
import api from '../data/api-index.json';

const lookups = [
  {name: 'func_800240DC_24CDC', path: 'functions', purpose: 'Read a game flag', detail: 'Query progression and encounter state.'},
  {name: 'D_800C7AB2', path: 'variables', purpose: 'Read the current room', detail: 'Check the room identifier and transition requirements.'},
  {name: 'func_80002040_2C40', path: 'functions', purpose: 'Observe the system update', detail: 'Understand the native system-step dispatcher.'},
];

export default function Home() {
  const referenceUrl = useBaseUrl('/reference/');
  const functionCount = api.filter(symbol => symbol.kind === 'function').length;

  return (
    <Layout title="Mod development reference" description="Mod development documentation for Mystical Ninja Starring Goemon Recompiled: native functions, external variables, and C examples.">
      <main className="home-container">
        <header className="home-header">
          <h1>Mystical Ninja Starring Goemon Recompiled</h1>
          <p className="home-purpose">Mod development reference</p>
          <p>Look up native functions and external variables for use in C. Each symbol page documents its interface, known behavior, usage requirements, and an example.</p>
        </header>

        <div className="home-layout">
          <div className="home-main">
            <section aria-labelledby="symbol-search-heading">
              <h2 id="symbol-search-heading">Find a function or variable</h2>
              <form className="home-search" action={referenceUrl} role="search" aria-label="Symbol lookup">
                <label className="home-search-label" htmlFor="home-symbol-query">Symbol name, address, or description</label>
                <div className="home-search-controls">
                  <input id="home-symbol-query" name="q" type="search" placeholder="e.g. D_800C7AB2 or room" />
                  <button className="button button--primary" type="submit">Search</button>
                </div>
              </form>
              <p className="home-coverage">Currently documents <Link to="/functions">{functionCount} functions</Link> and <Link to="/variables">{api.length - functionCount} variables</Link> from the US game.</p>
            </section>

            <section className="home-lookups" aria-labelledby="common-lookups-heading">
              <h2 id="common-lookups-heading">Common lookups</h2>
              <table>
                <thead><tr><th scope="col">Symbol</th><th scope="col">Use</th></tr></thead>
                <tbody>{lookups.map(symbol => (
                  <tr key={symbol.name}>
                    <td><Link to={`/${symbol.path}/${symbol.name}`}><code>{symbol.name}</code></Link></td>
                    <td><strong>{symbol.purpose}</strong><span>{symbol.detail}</span></td>
                  </tr>
                ))}</tbody>
              </table>
            </section>

            <section className="home-project" aria-labelledby="game-project-heading">
              <h2 id="game-project-heading">Game project</h2>
              <p>For the recompilation project’s source code, releases, and setup instructions, see <a href="https://github.com/klorfmorf/Goemon64Recomp">Goemon64Recomp on GitHub</a>.</p>
              <p className="home-project-note">This site is a separate reference for mod development.</p>
            </section>
          </div>

          <aside className="home-navigation" aria-label="Documentation sections">
            <h2>Reference</h2>
            <ul>
              <li><Link to="/reference">All symbols</Link><span>Search by name, address, or purpose.</span></li>
              <li><Link to="/functions">Functions</Link><span>Declarations, parameters, and return values.</span></li>
              <li><Link to="/variables">Variables</Link><span>Types, memory layout, and access.</span></li>
            </ul>
            <h2>Guides</h2>
            <ul>
              <li><Link to="/getting-started">Getting started</Link><span>Read declarations and use C examples.</span></li>
              <li><Link to="/native-lifecycle">Native lifecycle</Link><span>Room transitions, actors, and loaded resources.</span></li>
            </ul>
          </aside>
        </div>
      </main>
    </Layout>
  );
}
