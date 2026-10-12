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

export function renderMarkdown(source: string): string {
  const html = marked.parse(source ?? '', { async: false }) as string;
  return DOMPurify.sanitize(html, { USE_PROFILES: { html: true } });
}
