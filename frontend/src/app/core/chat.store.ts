import { Injectable, computed, effect, inject, signal } from '@angular/core';

import { ChatStreamService } from './chat-stream';
import { Activity, Attachment, Block, Conversation, Message, StreamEvent, Thumb, messageText } from './models';
import { readJson, storage, writeJson } from './storage';
import { UsageStore } from './usage.store';

const STORE_KEY = 'rb.conversations';
const ACTIVE_KEY = 'rb.activeConversation';
const MAX_CONVERSATIONS = 50;
const MAX_HISTORY_TURNS = 60;
const FLUSH_MS = 40;

const uid = () =>
  globalThis.crypto?.randomUUID?.() ?? `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;

/** A short, human description of a tool call for the activity list. */
export function describeTool(name: string, args: Record<string, unknown>): { label: string; detail?: string } {
  const str = (v: unknown) => (typeof v === 'string' ? v : '');
  switch (name) {
    case 'run_script': {
      const list = Array.isArray(args['args']) ? (args['args'] as unknown[]).map(String) : [];
      const quoted = list.map((a) => (/\s/.test(a) ? `"${a}"` : a)).join(' ');
      return {
        label: `Ran ${str(args['script']) || 'a script'}`,
        detail: `${str(args['skill_name'])} · ${quoted}`.trim(),
      };
    }
    case 'list_skills':
    case 'search_skills':
      return { label: 'Looked through the skill library' };
    case 'load_skill_resource':
      return {
        label: `Read ${str(args['file_path']) || str(args['path']) || 'a reference file'}`,
        detail: str(args['skill_name']),
      };
    case 'unload_skill':
      return { label: `Set aside ${str(args['skill_name'])}` };
    case 'write_file':
      return { label: `Saved ${str(args['filename']) || 'a file'}` };
    case 'read_file':
      return { label: `Read ${str(args['filename']) || 'a file'}` };
    default:
      return { label: name.replace(/_/g, ' ') };
  }
}

/** Conversations, kept in this browser only, and the turn that is currently streaming. */
@Injectable({ providedIn: 'root' })
export class ChatStore {
  private readonly stream = inject(ChatStreamService);
  private readonly usage = inject(UsageStore);
  private abort: AbortController | null = null;

  readonly conversations = signal<Conversation[]>(sanitize(readJson(storage('local'), STORE_KEY, [])));
  readonly activeId = signal<string | null>(readJson(storage('local'), ACTIVE_KEY, null));
  readonly busy = signal(false);
  readonly attachments = signal<Record<string, Attachment[]>>({});

  readonly active = computed(() => this.conversations().find((c) => c.id === this.activeId()) ?? null);
  readonly activeAttachments = computed(() => this.attachments()[this.activeId() ?? ''] ?? []);

  constructor() {
    effect(() => {
      const conversations = this.conversations();
      if (this.busy()) return;
      writeJson(
        storage('local'),
        STORE_KEY,
        conversations.filter((c) => c.messages.length),
      );
    });
    effect(() => writeJson(storage('local'), ACTIVE_KEY, this.activeId()));
  }

  create(skill: string | null = null, projectId: string | null = null): Conversation {
    const empty = this.conversations().find((c) => !c.messages.length && (c.projectId ?? null) === projectId);
    if (empty) {
      this.patch(empty.id, (c) => ({ ...c, skill, projectId, updatedAt: Date.now() }));
      this.activeId.set(empty.id);
      return { ...empty, skill, projectId };
    }
    const conversation: Conversation = {
      id: uid(),
      title: 'New chat',
      skill,
      projectId,
      deep: false,
      messages: [],
      updatedAt: Date.now(),
    };
    this.conversations.update((list) => [conversation, ...list].slice(0, MAX_CONVERSATIONS));
    this.activeId.set(conversation.id);
    return conversation;
  }

  select(id: string): void {
    if (!this.busy()) this.activeId.set(id);
  }

  remove(id: string): void {
    if (this.busy() && id === this.activeId()) this.stop();
    this.conversations.update((list) => list.filter((c) => c.id !== id));
    this.attachments.update(({ [id]: _, ...rest }) => rest);
    if (this.activeId() === id) this.activeId.set(this.conversations()[0]?.id ?? null);
  }

  clearAll(): void {
    this.stop();
    this.conversations.set([]);
    this.attachments.set({});
    this.activeId.set(null);
  }

  setSkill(skill: string | null): void {
    const id = this.activeId();
    if (id) this.patch(id, (c) => ({ ...c, skill }));
  }

  setProject(id: string, projectId: string | null): void {
    this.patch(id, (c) => ({ ...c, projectId }));
  }

  releaseProject(projectId: string): void {
    this.conversations.update((list) => list.map((c) => (c.projectId === projectId ? { ...c, projectId: null } : c)));
  }

  setDeep(deep: boolean): void {
    const id = this.activeId() ?? this.create().id;
    this.patch(id, (c) => ({ ...c, deep }));
  }

  rateMessage(messageId: string, feedback: Thumb): void {
    const id = this.activeId();
    if (!id) return;
    this.patch(id, (c) => ({
      ...c,
      messages: c.messages.map((m) => (m.id === messageId ? { ...m, feedback } : m)),
    }));
  }

  /** Copy this chat up to a message into a new conversation. */
  branchAt(messageId: string): Conversation | null {
    const current = this.active();
    if (!current || this.busy()) return null;
    const index = current.messages.findIndex((m) => m.id === messageId);
    if (index < 0) return null;
    const conversation: Conversation = {
      id: uid(),
      title: `${current.title} · branch`.slice(0, 80),
      skill: current.skill,
      projectId: current.projectId,
      deep: current.deep,
      messages: current.messages.slice(0, index + 1).map((m) => ({
        ...m,
        id: uid(),
        pending: false,
        blocks: m.blocks.map((b) => ({ ...b })),
      })),
      updatedAt: Date.now(),
    };
    this.conversations.update((list) => [conversation, ...list].slice(0, MAX_CONVERSATIONS));
    this.activeId.set(conversation.id);
    return conversation;
  }

  attach(files: Attachment[]): void {
    const id = this.activeId() ?? this.create().id;
    this.attachments.update((all) => {
      const merged = [...(all[id] ?? []).filter((a) => !files.some((f) => f.name === a.name)), ...files];
      return { ...all, [id]: merged.slice(0, 5) };
    });
  }

  detach(name: string): void {
    const id = this.activeId();
    if (id) this.attachments.update((all) => ({ ...all, [id]: (all[id] ?? []).filter((a) => a.name !== name) }));
  }

  stop(): void {
    this.abort?.abort();
  }

  async regenerate(): Promise<void> {
    const conversation = this.active();
    if (!conversation || this.busy()) return;
    const lastUser = [...conversation.messages].reverse().find((m) => m.role === 'user');
    if (!lastUser) return;
    const index = conversation.messages.indexOf(lastUser);
    this.patch(conversation.id, (c) => ({ ...c, messages: c.messages.slice(0, index) }));
    await this.send(messageText(lastUser));
  }

  async send(text: string): Promise<void> {
    text = text.trim();
    if (!text || this.busy()) return;
    const conversation = this.active() ?? this.create();
    const id = conversation.id;
    const files = this.attachments()[id] ?? [];

    const history = conversation.messages
      .map((m) => ({ role: m.role, content: messageText(m) }))
      .filter((m) => m.content)
      .slice(-MAX_HISTORY_TURNS);
    const user: Message = {
      id: uid(),
      role: 'user',
      blocks: [{ type: 'text', text }],
      attachments: files.length ? files.map((f) => f.name) : undefined,
    };
    const answer: Message = { id: uid(), role: 'assistant', blocks: [], pending: true };
    this.patch(id, (c) => ({
      ...c,
      title: c.messages.length ? c.title : titleFrom(text),
      messages: [...c.messages, user, answer],
      updatedAt: Date.now(),
    }));
    this.conversations.update((list) => [...list].sort((a, b) => b.updatedAt - a.updatedAt));

    this.busy.set(true);
    this.abort = new AbortController();
    const update = (fn: (m: Message) => Message) =>
      this.patch(id, (c) => ({ ...c, messages: c.messages.map((m) => (m.id === answer.id ? fn(m) : m)) }));

    let buffered = '';
    let timer: ReturnType<typeof setTimeout> | null = null;
    const flush = () => {
      if (timer) clearTimeout(timer);
      timer = null;
      if (!buffered) return;
      const delta = buffered;
      buffered = '';
      update((m) => ({ ...m, blocks: appendText(m.blocks, delta) }));
    };

    try {
      const request = {
        message: text,
        history,
        skill: conversation.skill,
        deep: conversation.deep,
        attachments: files.map(({ name, content, encoding }) => ({ name, content, encoding })),
      };
      for await (const event of this.stream.send(request, this.abort.signal)) {
        if (event.type === 'text') {
          buffered += event.delta;
          timer ??= setTimeout(flush, FLUSH_MS);
        } else {
          flush();
          update((m) => applyEvent(m, event));
        }
      }
    } catch (error) {
      if ((error as { name?: string }).name !== 'AbortError') {
        update((m) => ({ ...m, error: error instanceof Error ? error.message : 'The request failed.' }));
      }
    } finally {
      const aborted = this.abort?.signal.aborted ?? false;
      flush();
      update((m) => ({
        ...m,
        pending: false,
        blocks: m.blocks.map((b) => (b.type === 'activity' && b.status === 'running' ? { ...b, status: 'ok' } : b)),
      }));
      const finished = this.conversations()
        .find((c) => c.id === id)
        ?.messages.find((m) => m.id === answer.id);
      if (!aborted && finished && messageText(finished) && !finished.error) this.usage.completeTurn();
      this.abort = null;
      this.busy.set(false);
    }
  }

  private patch(id: string, fn: (c: Conversation) => Conversation): void {
    this.conversations.update((list) => list.map((c) => (c.id === id ? fn(c) : c)));
  }
}

function titleFrom(text: string): string {
  const line = text.split('\n')[0].trim();
  return line.length > 52 ? line.slice(0, 50).trimEnd() + '…' : line;
}

function appendText(blocks: Block[], delta: string): Block[] {
  const last = blocks.at(-1);
  if (last?.type === 'text') return [...blocks.slice(0, -1), { type: 'text', text: last.text + delta }];
  return [...blocks, { type: 'text', text: delta }];
}

export function applyEvent(message: Message, event: StreamEvent): Message {
  switch (event.type) {
    case 'text':
      return { ...message, blocks: appendText(message.blocks, event.delta) };
    case 'skill_loaded': {
      const activity: Activity = {
        type: 'activity',
        id: event.id ?? uid(),
        kind: 'skill',
        name: event.skill,
        label: `Using ${event.skill}`,
        status: 'ok',
      };
      return { ...message, blocks: [...message.blocks, activity] };
    }
    case 'tool_call': {
      const activity: Activity = {
        type: 'activity',
        id: event.id ?? uid(),
        kind: 'tool',
        name: event.name,
        ...describeTool(event.name, event.args ?? {}),
        status: 'running',
      };
      return { ...message, blocks: [...message.blocks, activity] };
    }
    case 'tool_result':
      return {
        ...message,
        blocks: message.blocks.map((b) =>
          b.type === 'activity' && (b.id === event.id || (b.status === 'running' && b.name === event.name))
            ? { ...b, status: event.ok ? 'ok' : 'error', preview: event.preview }
            : b,
        ),
      };
    case 'error':
      return { ...message, error: event.message };
    default:
      return message;
  }
}

function sanitize(value: unknown): Conversation[] {
  if (!Array.isArray(value)) return [];
  return value
    .filter((c): c is Conversation => !!c && typeof c.id === 'string' && Array.isArray(c.messages))
    .map((c) => ({
      ...c,
      skill: c.skill ?? null,
      projectId: c.projectId ?? null,
      deep: !!c.deep,
      messages: c.messages.filter((m) => m && Array.isArray(m.blocks)).map((m) => ({ ...m, pending: false })),
    }));
}
