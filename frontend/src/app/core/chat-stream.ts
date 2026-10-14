import { Injectable, inject } from '@angular/core';

import { Attachment, StreamEvent } from './models';
import { SettingsStore } from './settings.store';

export interface ChatRequestBody {
  message: string;
  history: { role: 'user' | 'assistant'; content: string }[];
  skill: string | null;
  deep?: boolean;
  attachments: Pick<Attachment, 'name' | 'content' | 'encoding'>[];
}

@Injectable({ providedIn: 'root' })
export class ChatStreamService {
  private readonly settings = inject(SettingsStore);

  async *send(body: ChatRequestBody, signal: AbortSignal): AsyncGenerator<StreamEvent> {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...this.settings.credentialHeaders(),
      },
      body: JSON.stringify(body),
      signal,
    });

    if (!response.ok) {
      let message = `The server returned an error (${response.status}).`;
      let fromServer = false;
      try {
        const payload = (await response.json()) as { message?: string };
        if (payload.message) {
          message = payload.message;
          fromServer = true;
        }
      } catch {
        /* not JSON */
      }
      if (response.status === 413 && !fromServer) {
        // Vercel answers oversized bodies itself with a non-JSON FUNCTION_PAYLOAD_TOO_LARGE.
        message =
          'This message is too large to send. Remove some attachments or start a new chat.';
      }
      yield { type: 'error', status: response.status, message };
      return;
    }

    const reader = response.body?.getReader();
    if (!reader) {
      yield { type: 'error', message: 'The server closed the stream unexpectedly.' };
      return;
    }

    const decoder = new TextDecoder();
    let buffer = '';
    while (true) {
      const { done, value } = await reader.read();
      buffer += decoder.decode(value || new Uint8Array(), { stream: !done });
      const chunks = buffer.split('\n\n');
      buffer = chunks.pop() ?? '';
      for (const chunk of chunks) {
        const event = parseSse(chunk);
        if (event) yield event;
      }
      if (done) break;
    }
    const last = parseSse(buffer);
    if (last) yield last;
  }
}

export function parseSse(chunk: string): StreamEvent | null {
  let eventType = '';
  const data: string[] = [];
  for (const raw of chunk.split('\n')) {
    const line = raw.endsWith('\r') ? raw.slice(0, -1) : raw;
    if (line.startsWith('event:')) eventType = line.slice(6).trim();
    else if (line.startsWith('data:')) data.push(line.slice(5).trimStart());
  }
  if (!data.length) return null;
  try {
    const parsed = JSON.parse(data.join('\n')) as StreamEvent;
    if (eventType && parsed.type !== eventType) return { ...parsed, type: eventType } as StreamEvent;
    return parsed;
  } catch {
    return eventType === 'error' ? { type: 'error', message: data.join('\n') } : null;
  }
}
