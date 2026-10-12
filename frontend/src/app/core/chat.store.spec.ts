import { applyEvent, describeTool } from './chat.store';
import { Message, messageText } from './models';

const empty = (): Message => ({ id: 'm', role: 'assistant', blocks: [], pending: true });

describe('applyEvent', () => {
  it('builds text and activity blocks in the order events arrive', () => {
    let m = empty();
    m = applyEvent(m, { type: 'skill_loaded', id: 'a', skill: 'paper-search' });
    m = applyEvent(m, { type: 'tool_call', id: 'b', name: 'run_script', args: { skill_name: 'paper-search', script: 'search_papers.py', args: ['graph neural networks', '--limit', '5'] } });
    m = applyEvent(m, { type: 'tool_result', id: 'b', name: 'run_script', ok: true, preview: '1. A paper' });
    m = applyEvent(m, { type: 'text', delta: 'Here are ' });
    m = applyEvent(m, { type: 'text', delta: 'the papers.' });

    expect(m.blocks.map((b) => b.type)).toEqual(['activity', 'activity', 'text']);
    expect(m.blocks[1]).toEqual(jasmine.objectContaining({
      label: 'Ran search_papers.py', status: 'ok', preview: '1. A paper',
      detail: 'paper-search · "graph neural networks" --limit 5',
    }));
    expect(messageText(m)).toBe('Here are the papers.');
  });

  it('marks a failed tool and records a stream error', () => {
    let m = applyEvent(empty(), { type: 'tool_call', id: 'x', name: 'read_file', args: { filename: 'a.bib' } });
    m = applyEvent(m, { type: 'tool_result', id: 'x', name: 'read_file', ok: false, preview: 'no such file' });
    m = applyEvent(m, { type: 'error', message: 'The provider rejected this API key.' });
    expect(m.blocks[0]).toEqual(jasmine.objectContaining({ status: 'error', label: 'Read a.bib' }));
    expect(m.error).toBe('The provider rejected this API key.');
  });
});

describe('describeTool', () => {
  it('falls back to a readable name for tools it does not know', () => {
    expect(describeTool('some_new_tool', {})).toEqual({ label: 'some new tool' });
  });
});
