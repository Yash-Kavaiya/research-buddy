/** A web source cited in an answer, shown in the Sources rail. */
export interface Source {
  n: number;
  url: string;
  domain: string;
  title: string;
  snippet: string;
}

const URL_RE = /https?:\/\/[^\s<>()\]"'`]+[^\s<>()\]"'`.,;:!?]/g;
const DOI_RE = /\b(?:doi:\s*)?(10\.\d{4,9}\/[^\s<>()\]"'`]+[^\s<>()\]"'`.,;:!?])/gi;
const MD_LINK_RE = /\[([^\]\n]{1,200})\]\((https?:\/\/[^\s)]+)\)/g;
const NUMBERED_RE = /^\s*(?:[-*]\s*)?(?:\[(\d{1,3})\]|(\d{1,3})[.)])\s+(.+)$/;

/**
 * Collect the sources an answer cites. Numbered reference lines ("[3] ... https://...",
 * "3. ... doi:10...") keep their numbers so inline [3] markers line up; any other links
 * are numbered after them in order of appearance.
 */
export function extractSources(text: string): Source[] {
  const byUrl = new Map<string, Source>();
  const used = new Set<number>();
  const loose: { url: string; title: string; line: string }[] = [];

  for (const line of (text ?? '').split('\n')) {
    const links = linksIn(line);
    if (!links.length) continue;
    const numbered = NUMBERED_RE.exec(line);
    const n = numbered ? Number(numbered[1] ?? numbered[2]) : 0;
    links.forEach((link, i) => {
      if (byUrl.has(link.url)) return;
      if (i === 0 && n && !used.has(n)) {
        used.add(n);
        byUrl.set(link.url, makeSource(n, link.url, link.title, line));
      } else {
        loose.push({ ...link, line });
      }
    });
  }

  let next = 1;
  for (const link of loose) {
    if (byUrl.has(link.url)) continue;
    while (used.has(next)) next++;
    used.add(next);
    byUrl.set(link.url, makeSource(next, link.url, link.title, link.line));
  }
  return [...byUrl.values()].sort((a, b) => a.n - b.n);
}

function linksIn(line: string): { url: string; title: string }[] {
  const found: { url: string; title: string; at: number }[] = [];
  const seen = new Set<string>();
  const add = (url: string, title: string, at: number) => {
    const clean = url.replace(/[)\]]+$/, '');
    if (seen.has(clean)) return;
    seen.add(clean);
    found.push({ url: clean, title, at });
  };
  for (const m of line.matchAll(MD_LINK_RE)) add(m[2], m[1].trim(), m.index ?? 0);
  for (const m of line.matchAll(URL_RE)) add(m[0], '', m.index ?? 0);
  for (const m of line.matchAll(DOI_RE)) {
    if (/https?:\/\/[^\s]*$/.test(line.slice(0, m.index ?? 0))) continue; // already part of a URL
    add(`https://doi.org/${m[1]}`, '', m.index ?? 0);
  }
  return found.sort((a, b) => a.at - b.at).map(({ url, title }) => ({ url, title }));
}

function makeSource(n: number, url: string, title: string, line: string): Source {
  const domain = domainOf(url);
  const snippet = plain(line).slice(0, 220);
  return { n, url, domain, title: title || titleFrom(snippet, domain), snippet };
}

export function domainOf(url: string): string {
  try {
    return new URL(url).hostname.replace(/^www\./, '');
  } catch {
    return url;
  }
}

/** Strip markdown, URLs, and the leading reference number from a line. */
function plain(line: string): string {
  return line
    .replace(MD_LINK_RE, '$1')
    .replace(URL_RE, '')
    .replace(DOI_RE, '')
    .replace(NUMBERED_RE, '$3')
    .replace(/[*_`>#]/g, '')
    .replace(/\b(?:URL|Link|Available at|Retrieved from)\s*:?\s*$/i, '')
    .replace(/\s*[-–—:,;.]\s*$/, '')
    .replace(/\s+/g, ' ')
    .trim();
}

function titleFrom(snippet: string, domain: string): string {
  if (!snippet) return domain;
  const quoted = /[“"]([^”"]{8,160})[”"]/.exec(snippet);
  if (quoted) return quoted[1];
  return snippet.length > 90 ? snippet.slice(0, 88).trimEnd() + '…' : snippet;
}
