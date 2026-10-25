// Build: concatenate src/*.html, pre-render KaTeX math, write dist/binder.html.
// Math delimiters: \( ... \) inline, \[ ... \] display.
// Page-number placeholders: {{p:ID}} are replaced from dist/pages.json (written by stamp.py).
const fs = require('fs');
const path = require('path');
const katex = require('/projects/sandbox/.build/node_modules/katex');

const root = __dirname;
const srcDir = path.join(root, 'src');
const dist = path.join(root, 'dist');
fs.mkdirSync(dist, { recursive: true });

const files = fs.readdirSync(srcDir).filter(f => f.endsWith('.html')).sort();
let body = files.map(f => fs.readFileSync(path.join(srcDir, f), 'utf8')).join('\n');

const macros = { '\\P': '\\operatorname{P}', '\\E': '\\operatorname{E}', '\\Var': '\\operatorname{Var}' };
let errors = 0;
const render = (tex, display) => {
  tex = tex.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&').replace(/&nbsp;/g, ' ');
  try {
    return katex.renderToString(tex, { displayMode: display, throwOnError: true, macros, strict: false });
  } catch (e) {
    errors++;
    console.error('KaTeX error:', e.message, '\n   in:', tex.slice(0, 120));
    return `<span style="color:red">[MATH ERROR: ${tex}]</span>`;
  }
};
body = body.replace(/\\\[([\s\S]+?)\\\]/g, (_, t) => render(t, true));
body = body.replace(/\\\(([\s\S]+?)\\\)/g, (_, t) => render(t, false));

// page refs
const pagesFile = path.join(dist, 'pages.json');
const pages = fs.existsSync(pagesFile) ? JSON.parse(fs.readFileSync(pagesFile, 'utf8')) : {};
const missing = new Set();
body = body.replace(/\{\{p:([A-Za-z0-9_-]+)\}\}/g, (_, id) => {
  if (pages[id] === undefined) { missing.add(id); return '<span class="pref">p.&#8199;&#8199;</span>'; }
  return `<span class="pref">p.${pages[id]}</span>`;
});
// anchors: <a-id> markers become tiny white text tokens for stamp.py to locate.
body = body.replace(/<anchor id="([A-Za-z0-9_-]+)"\s*(?:label="([^"]*)")?\s*\/>/g,
  (_, id, label) => `<span class="anchor">@@${id}|${label || ''}@@</span>`);

const css = fs.readFileSync(path.join(root, 'style.css'), 'utf8');
const katexCss = 'file:///projects/sandbox/.build/node_modules/katex/dist/katex.min.css';
const html = `<!doctype html><html lang="en"><head><meta charset="utf-8">
<link rel="stylesheet" href="${katexCss}"><style>${css}</style></head><body>${body}</body></html>`;
fs.writeFileSync(path.join(dist, 'binder.html'), html);
console.log(`built ${files.length} files, math errors: ${errors}, unresolved page refs: ${missing.size ? [...missing].join(',') : 0}`);
if (errors) process.exit(1);
