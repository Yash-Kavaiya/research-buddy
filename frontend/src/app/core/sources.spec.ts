import { extractSources } from './sources';

describe('extractSources', () => {
  it('keeps the numbers of a reference list so inline markers line up', () => {
    const text = [
      'RAG helps with fresh knowledge [2] and fine-tuning with style [1].',
      '',
      '## References',
      '[1] Hu et al. “LoRA: Low-Rank Adaptation” https://arxiv.org/abs/2106.09685',
      '2. Lewis et al., Retrieval-Augmented Generation, doi:10.48550/arXiv.2005.11401',
    ].join('\n');
    const sources = extractSources(text);
    expect(sources.map((s) => s.n)).toEqual([1, 2]);
    expect(sources[0].domain).toBe('arxiv.org');
    expect(sources[0].title).toBe('LoRA: Low-Rank Adaptation');
    expect(sources[1].url).toBe('https://doi.org/10.48550/arXiv.2005.11401');
  });

  it('numbers loose links in order and skips duplicates', () => {
    const text = 'See [the docs](https://www.example.org/a) and https://pubmed.ncbi.nlm.nih.gov/123/. Again https://www.example.org/a';
    const sources = extractSources(text);
    expect(sources.length).toBe(2);
    expect(sources[0]).toEqual(jasmine.objectContaining({ n: 1, domain: 'example.org', title: 'the docs' }));
    expect(sources[1]).toEqual(jasmine.objectContaining({ n: 2, url: 'https://pubmed.ncbi.nlm.nih.gov/123/' }));
  });

  it('returns nothing for text without links', () => {
    expect(extractSources('No links here [1].')).toEqual([]);
  });
});
