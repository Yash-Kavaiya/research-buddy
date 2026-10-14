import { markCitations, referenceLinesToList, renderMarkdown } from './markdown';

describe('answer markdown', () => {
  it('turns bracketed reference lines into a numbered list, outside code fences', () => {
    const text = '## References\n[1] A paper\n[2] Another\n```\n[3] not a ref\n```';
    expect(referenceLinesToList(text)).toBe('## References\n1. A paper\n2. Another\n```\n[3] not a ref\n```');
  });

  it('renders [n] markers as citation chips but leaves code and links alone', () => {
    const html = markCitations('<p>Claim [2] and [1, 3].</p><pre><code>x[1]</code></pre><a href="#">[4]</a>');
    const root = document.createElement('div');
    root.innerHTML = html;
    expect(Array.from(root.querySelectorAll('.cite')).map((c) => c.getAttribute('data-cite'))).toEqual(['2', '1', '3']);
    expect(root.querySelector('code')?.textContent).toBe('x[1]');
    expect(root.querySelector('a')?.textContent).toBe('[4]');
  });

  it('wraps tables so they can scroll inside a card', () => {
    expect(renderMarkdown('| a | b |\n|---|---|\n| 1 | 2 |')).toContain('<div class="table-wrap"><table>');
  });
});
