import { parseSse } from './chat-stream';

describe('parseSse', () => {
  it('returns complete events and keeps the unfinished tail', () => {
    const { events, rest } = parseSse(
      'event: text\ndata: {"type":"text","delta":"Hel"}\n\nevent: text\ndata: {"type":"text","delta":"lo"}\n\nevent: done\ndata: {"ty',
    );
    expect(events).toEqual([
      { type: 'text', delta: 'Hel' },
      { type: 'text', delta: 'lo' },
    ]);
    expect(rest).toBe('event: done\ndata: {"ty');
  });

  it('joins a tail with the next chunk', () => {
    const first = parseSse('event: done\ndata: {"ty');
    const second = parseSse(first.rest + 'pe":"done"}\n\n');
    expect(second.events).toEqual([{ type: 'done' }]);
    expect(second.rest).toBe('');
  });

  it('accepts CRLF line endings and skips malformed frames', () => {
    const { events } = parseSse('data: not json\r\n\r\ndata: {"type":"done"}\r\n\r\n');
    expect(events).toEqual([{ type: 'done' }]);
  });
});
