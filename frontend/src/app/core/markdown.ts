import DOMPurify from 'dompurify';
import hljs from 'highlight.js/lib/core';
import bash from 'highlight.js/lib/languages/bash';
import json from 'highlight.js/lib/languages/json';
import latex from 'highlight.js/lib/languages/latex';
import markdownLang from 'highlight.js/lib/languages/markdown';
import python from 'highlight.js/lib/languages/python';
import r from 'highlight.js/lib/languages/r';
import yaml from 'highlight.js/lib/languages/yaml';
import { Marked } from 'marked';
import { markedHighlight } from 'marked-highlight';
import markedKatex from 'marked-katex-extension';

hljs.registerLanguage('bash', bash);
hljs.registerLanguage('json', json);
hljs.registerLanguage('latex', latex);
hljs.registerLanguage('markdown', markdownLang);
hljs.registerLanguage('python', python);
hljs.registerLanguage('r', r);
hljs.registerLanguage('yaml', yaml);
hljs.registerAliases(['sh', 'shell', 'console'], { languageName: 'bash' });
hljs.registerAliases(['tex', 'bibtex', 'bib'], { languageName: 'latex' });
hljs.registerAliases(['py'], { languageName: 'python' });
hljs.registerAliases(['md'], { languageName: 'markdown' });

const marked = new Marked(
  { gfm: true, breaks: false },
  markedHighlight({
    highlight: (code, lang) => (lang && hljs.getLanguage(lang) ? hljs.highlight(code, { language: lang }).value : escapeHtml(code)),
  }),
  markedKatex({ throwOnError: false, nonStandard: true }),
);

marked.use({
  renderer: {
    // Wide tables scroll inside their own box instead of stretching the page.
    table(token) {
      const header = token.header.map((cell) => `<th>${this.parser.parseInline(cell.tokens)}</th>`).join('');
      const rows = token.rows
        .map((row) => `<tr>${row.map((cell) => `<td>${this.parser.parseInline(cell.tokens)}</td>`).join('')}</tr>`)
        .join('');
      return `<div class="table-wrap"><table><thead><tr>${header}</tr></thead><tbody>${rows}</tbody></table></div>`;
    },
  },
});

DOMPurify.addHook('afterSanitizeAttributes', (node) => {
  if (node instanceof HTMLAnchorElement && node.hasAttribute('href')) {
    node.setAttribute('target', '_blank');
    node.setAttribute('rel', 'noopener noreferrer');
  }
});

function escapeHtml(text: string): string {
  return text.replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' })[c]!);
}

/** Models often write \( \) and \[ \] for maths; KaTeX's Markdown extension reads $ and $$. */
function normalizeMath(source: string): string {
  return source
    .split(/(```[\s\S]*?```|`[^`\n]*`)/g)
    .map((part, i) =>
      i % 2
        ? part
        : part
            .replace(/\\\[([\s\S]+?)\\\]/g, (_, body) => `\n$$\n${body.trim()}\n$$\n`)
            .replace(/\\\(([\s\S]+?)\\\)/g, (_, body) => `$${body.trim()}$`),
    )
    .join('');
}

/** Markdown to sanitized HTML: GitHub tables, highlighted code, and KaTeX maths. */
export function renderMarkdown(source: string): string {
  const html = marked.parse(normalizeMath(source), { async: false });
  return DOMPurify.sanitize(html, { FORBID_TAGS: ['style', 'form', 'input', 'button'], FORBID_ATTR: ['id', 'name'] });
}
