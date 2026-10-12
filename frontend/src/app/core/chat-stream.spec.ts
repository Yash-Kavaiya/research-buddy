import { parseSse } from './chat-stream';

describe('parseSse', () => {
  it('reads one server-sent event', () => {
    expect(parseSse('event: text\ndata: {"type":"text","delta":"Hel"}')).toEqual({
      type: 'text',
      delta: 'Hel',
    });
  });

  it('accepts CRLF line endings', () => {
    expect(parseSse('event: done\r\ndata: {"type":"done"}\r\n')).toEqual({ type: 'done' });
  });

  it('skips a frame that is not JSON', () => {
    expect(parseSse('data: not json')).toBeNull();
  });
});
