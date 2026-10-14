import DOMPurify from 'dompurify';
import hljs from 'highlight.js/lib/core';
import bash from 'highlight.js/lib/languages/bash';
import javascript from 'highlight.js/lib/languages/javascript';
import json from 'highlight.js/lib/languages/json';
import latex from 'highlight.js/lib/languages/latex';
import python from 'highlight.js/lib/languages/python';
import xml from 'highlight.js/lib/languages/xml';
import { marked } from 'marked';
import { markedHighlight } from 'marked-highlight';
import markedKatex from 'marked-katex-extension';

hljs.registerLanguage('python', python);
hljs.registerLanguage('py', python);
hljs.registerLanguage('bash', bash);
hljs.registerLanguage('sh', bash);
hljs.registerLanguage('json', json);
hljs.registerLanguage('javascript', javascript);
hljs.registerLanguage('js', javascript);
hljs.registerLanguage('xml', xml);
hljs.registerLanguage('html', xml);
hljs.registerLanguage('latex', latex);
hljs.registerLanguage('tex', latex);
hljs.registerLanguage('bibtex', latex);

marked.use(
  markedKatex({
    throwOnError: false,
    nonStandard: true,
  }),
);

marked.use(
  markedHighlight({
    langPrefix: 'hljs language-',
    highlight(code, lang) {
      if (lang && hljs.getLanguage(lang)) {
        return hljs.highlight(code, { language: lang }).value;
      }
      return hljs.highlightAuto(code).value;
    },
  }),
);

marked.setOptions({ gfm: true, breaks: false });

DOMPurify.addHook('afterSanitizeAttributes', (node) => {
  if (node.tagName !== 'A') return;
  node.setAttribute('target', '_blank');
  node.setAttribute('rel', 'noopener noreferrer');
});

export function renderMarkdown(source: string, cites = false): string {
  const text = cites ? referenceLinesToList(source ?? '') : (source ?? '');
  const html = marked.parse(text, { async: false }) as string;
  const clean = DOMPurify.sanitize(html, { USE_PROFILES: { html: true }, ADD_ATTR: ['target', 'rel'] });
  const wrapped = clean.replace(/<table>/g, '<div class="table-wrap"><table>').replace(/<\/table>/g, '</table></div>');
  return cites ? markCitations(wrapped) : wrapped;
}

const REF_LINE = /^\s*\[(\d{1,3})\]\s+(.*)$/;

/**
 * Models often write a reference list as "[1] ..." lines with no blank lines between them,
 * which markdown folds into one paragraph. Turn such lines into a numbered list.
 */
export function referenceLinesToList(source: string): string {
  let fenced = false;
  return source
    .split('\n')
    .map((line) => {
      if (/^\s*(```|~~~)/.test(line)) fenced = !fenced;
      const m = fenced ? null : REF_LINE.exec(line);
      return m ? `${m[1]}. ${m[2]}` : line;
    })
    .join('\n');
}

const CITE_RE = /\[(\d{1,3}(?:\s*[,–-]\s*\d{1,3})*)\]/g;

/** Turn "[2]" or "[1, 3]" in answer prose into citation chips that the Sources rail can match. */
export function markCitations(html: string): string {
  if (typeof document === 'undefined' || !html.includes('[')) return html;
  const root = document.createElement('template');
  root.innerHTML = html;
  const walker = document.createTreeWalker(root.content, NodeFilter.SHOW_TEXT);
  const targets: Text[] = [];
  for (let node = walker.nextNode(); node; node = walker.nextNode()) {
    const text = node as Text;
    if (!CITE_RE.test(text.data)) continue;
    CITE_RE.lastIndex = 0;
    if (text.parentElement?.closest('code, pre, a, .katex')) continue;
    targets.push(text);
  }
  for (const text of targets) {
    const frag = document.createDocumentFragment();
    let last = 0;
    for (const m of text.data.matchAll(CITE_RE)) {
      frag.append(text.data.slice(last, m.index));
      for (const n of expand(m[1])) {
        const sup = document.createElement('sup');
        sup.className = 'cite';
        sup.dataset['cite'] = String(n);
        sup.textContent = String(n);
        frag.append(sup);
      }
      last = (m.index ?? 0) + m[0].length;
    }
    frag.append(text.data.slice(last));
    text.replaceWith(frag);
  }
  return root.innerHTML;
}

function expand(spec: string): number[] {
  const out: number[] = [];
  for (const part of spec.split(',')) {
    const [a, b] = part.split(/[–-]/).map((x) => Number(x.trim()));
    if (b && b > a && b - a < 20) for (let i = a; i <= b; i++) out.push(i);
    else out.push(a);
  }
  return out;
}
