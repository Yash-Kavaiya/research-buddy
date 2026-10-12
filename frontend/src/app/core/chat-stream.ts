import { Injectable, inject } from '@angular/core';

import { Attachment, StreamEvent } from './models';
import { SettingsStore } from './settings.store';

export interface ChatRequest {
  message: string;
  history: { role: 'user' | 'assistant'; content: string }[];
  skill: string | null;
  attachments: Pick<Attachment, 'name' | 'content' | 'encoding'>[];
}

/**
 * Split a Server-Sent Events buffer into complete events.
 * Returns the parsed events and the unfinished tail to carry into the next chunk.
 */
export function parseSse(buffer: string): { events: StreamEvent[]; rest: string } {
  const events: StreamEvent[] = [];
  const frames = buffer.replace(/\r\n/g, '\n').split('\n\n');
  const rest = frames.pop() ?? '';
  for (const frame of frames) {
    const data = frame
      .split('\n')
      .filter((line) => line.startsWith('data:'))
      .map((line) => line.slice(5).replace(/^ /, ''))
      .join('\n');
    if (!data) continue;
    try {
      events.push(JSON.parse(data) as StreamEvent);
    } catch {
      /* skip a malformed frame instead of ending the stream */
    }
  }
  return { events, rest };
}

@Injectable({ providedIn: 'root' })
export class ChatStreamService {
  private readonly settings = inject(SettingsStore);

  /** Send one message and yield the agent's events as they arrive. */
  async *send(request: ChatRequest, signal: AbortSignal): AsyncGenerator<StreamEvent> {
    let response: Response;
    try {
      response = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...this.settings.credentialHeaders() },
        body: JSON.stringify(request),
        signal,
      });
    } catch (error) {
      if (signal.aborted) return;
      yield { type: 'error', message: 'Could not reach the server. Check your connection and try again.' };
      return;
    }

    if (!response.ok || !response.body) {
      let message = `The server returned an error (${response.status}).`;
      try {
        message = (await response.json()).message ?? message;
      } catch {
        if (response.status === 413) message = 'The request is too large. Remove an attachment or start a new chat.';
        if (response.status === 504) message = 'The request timed out. Try a smaller task.';
      }
      yield { type: 'error', message, status: response.status };
      return;
    }

    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let buffer = '';
    let finished = false;
    try {
      while (true) {
        const { done, value } = await reader.read();
        if (done) break;
        const parsed = parseSse(buffer + decoder.decode(value, { stream: true }));
        buffer = parsed.rest;
        for (const event of parsed.events) {
          if (event.type === 'done' || event.type === 'error') finished = true;
          yield event;
        }
      }
    } catch {
      if (signal.aborted) return;
    }
    if (!finished && !signal.aborted) {
      yield { type: 'error', message: 'The connection closed before the answer finished. Try again.' };
    }
  }
}
