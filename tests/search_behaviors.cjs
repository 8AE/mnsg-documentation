/* Exercise the components' actual search/navigation callbacks, without copying
 * their algorithms. Browser QA remains responsible for React hydration and DOM.
 * Babel is already supplied by the Docusaurus toolchain. */
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const parser = require('@babel/parser');
const traverse = require('@babel/traverse').default;
const generate = require('@babel/generator').default;

const root = path.resolve(__dirname, '..');
const api = JSON.parse(fs.readFileSync(path.join(root, 'src/data/api-index.json')));
const readAst = file => parser.parse(fs.readFileSync(path.join(root, file), 'utf8'), {sourceType: 'module', plugins: ['jsx']});
const searchAst = readAst('src/theme/SearchBar/index.jsx');
const referenceAst = readAst('src/pages/reference.jsx');
function selected(ast, predicate) {
  let found;
  traverse(ast, {enter(p) { if (!found && predicate(p.node)) found = p.node; }});
  assert.ok(found, 'Expected component callback is present');
  return found;
}
const hookCallback = (ast, name) => selected(ast, n => n.type === 'CallExpression' && n.callee.name === name).arguments[0];
const variable = (ast, name) => selected(ast, n => n.type === 'VariableDeclarator' && n.id.name === name).init;
function evaluate(node, values) {
  return new Function(...Object.keys(values), `return (${generate(node).code});`)(...Object.values(values));
}
const normalize = evaluate(variable(searchAst, 'normalize'), {});
const headerHits = query => evaluate(hookCallback(searchAst, 'useMemo'), {api, query, normalize})();
const catalogHits = (query, kind = '') => evaluate(hookCallback(referenceAst, 'useMemo'), {api, query, kind})();

test('exact native names outrank descriptions that mention the same symbol', () => {
  for (const name of ['func_800240DC_24CDC', 'D_800C7AB2', 'func_80002040_2C40']) {
    assert.equal(headerHits(name)[0].name, name);
    assert.equal(catalogHits(name)[0].name, name);
    assert.equal(headerHits(name.toLowerCase())[0].name, name);
  }
});

test('escaped underscores, partial addresses, multiple words, and type filters work', () => {
  assert.equal(headerHits('func\\_800240DC\\_24CDC')[0].name, 'func_800240DC_24CDC');
  assert.ok(catalogHits('800C7AB2').some(s => s.name === 'D_800C7AB2'));
  const flags = catalogHits('flag read', 'function');
  assert.ok(flags.length > 0);
  assert.ok(flags.every(s => s.kind === 'function'));
  assert.equal(catalogHits('D_800C7AB2', 'function').length, 0);
  assert.equal(catalogHits('D_800C7AB2', 'variable')[0].name, 'D_800C7AB2');
  assert.equal(catalogHits('', 'variable').length, api.filter(s => s.kind === 'variable').length);
  assert.equal(headerHits('zzzz_no_native_symbol_zzzz').length, 0);
});

test('decoded room names are searchable in the header and symbol catalog', () => {
  const room = api.find(s => s.name === 'D_800C7AB2');
  assert.ok(room.values.includes('Bizen Bridge'));
  assert.equal(headerHits('Bizen Bridge')[0].name, room.name);
  assert.equal(catalogHits('Bizen Bridge', 'variable')[0].name, room.name);
});

test('catalog updates synchronize router location and preserve the Pages path', () => {
  const updateNode = selected(referenceAst, n => n.type === 'FunctionDeclaration' && n.id.name === 'update');
  const location = {pathname: '/mnsg-documentation/reference/', search: ''};
  const state = {query: '', kind: ''};
  let routerUpdates = 0;
  const history = {replace(next) {routerUpdates++; Object.assign(location, next);}};
  const window = {location, history: {replaceState() {throw new Error('Bypassing React Router leaves useLocation stale');}}};
  const update = evaluate(updateNode, {location, history, window, setQuery: q => {state.query=q;}, setKind: k => {state.kind=k;}});
  update('room & flag', 'variable');
  assert.equal(routerUpdates, 1);
  assert.equal(location.pathname, '/mnsg-documentation/reference/');
  assert.equal(new URLSearchParams(location.search).get('q'), 'room & flag');
  assert.equal(new URLSearchParams(location.search).get('kind'), 'variable');
  assert.deepEqual(state, {query:'room & flag', kind:'variable'});
  update('', '');
  assert.equal(location.search, '');
  assert.equal(routerUpdates, 2);
});

test('navigation, Back, and query hydration restore both filters from the URL', () => {
  const location = {pathname: '/mnsg-documentation/reference/', search: '?q=D_800C7AB2&kind=variable'};
  const state = {};
  const hydrate = evaluate(hookCallback(referenceAst, 'useEffect'), {location, setQuery: q => {state.query=q;}, setKind: k => {state.kind=k;}});
  hydrate();
  assert.deepEqual(state, {query:'D_800C7AB2', kind:'variable'});
  location.search = '';
  hydrate();
  assert.deepEqual(state, {query:'', kind:''});
  location.search = '?q=flag&kind=invalid';
  hydrate();
  assert.deepEqual(state, {query:'flag', kind:''});
});

test('Escape restores input focus before closing keyboard search suggestions', () => {
  const suggestion = {};
  let focused = 'suggestion';
  let open = true;
  const input = {current: {focus() {focused='input';}}};
  const container = {current: {contains(target) {return target === suggestion;}}};
  const document = {activeElement: suggestion};
  const keyboard = evaluate(variable(searchAst, 'keyboard'), {input, container, document, setOpen: value => {open=value;}});
  keyboard({key:'Escape', target:suggestion});
  assert.equal(focused, 'input');
  assert.equal(open, false);
});

test('browser search data and published search data are the same native catalog', () => {
  const published = JSON.parse(fs.readFileSync(path.join(root, 'static/api-index.json')));
  assert.deepEqual(api, published);
  for (const entry of api) {
    assert.equal(entry.url, `/${entry.kind === 'function' ? 'functions' : 'variables'}/${entry.name}/`);
    assert.equal(entry.projects, undefined);
    assert.equal(entry.evidence, undefined);
  }
});
