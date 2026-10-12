import {
  ChangeDetectionStrategy, Component, ElementRef, computed, effect, inject, input, signal, untracked, viewChild,
} from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { ChatStore } from '../../core/chat.store';
import { Attachment, Conversation, Message, messageText } from '../../core/models';
import { SettingsStore } from '../../core/settings.store';
import { Icon } from '../../shared/icon';
import { Markdown } from '../../shared/markdown';

const MAX_FILES = 5;
const MAX_FILE_BYTES = 3_000_000;
const TEXT_TYPES = /\.(bib|csv|tsv|tex|txt|md|json|ris|ya?ml)$/i;

@Component({
  selector: 'app-workspace',
  imports: [RouterLink, Icon, Markdown],
  templateUrl: './workspace.html',
  styleUrl: './workspace.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Workspace {
  private readonly api = inject(ApiService);
  private readonly router = inject(Router);
  protected readonly chats = inject(ChatStore);
  protected readonly settings = inject(SettingsStore);

  /** Bound from ?skill= and ?prompt=, set by links on the landing and skill pages. */
  readonly skill = input<string>();
  readonly prompt = input<string>();

  private readonly scroller = viewChild<ElementRef<HTMLElement>>('scroller');
  private readonly textarea = viewChild<ElementRef<HTMLTextAreaElement>>('box');

  protected readonly catalog = toSignal(this.api.catalog().pipe(catchError(() => of(null))), { initialValue: null });
  protected readonly draft = signal('');
  protected readonly sidebarOpen = signal(false);
  protected readonly fileError = signal('');
  protected readonly copied = signal<string | null>(null);

  protected readonly conversation = this.chats.active;
  protected readonly messages = computed(() => this.conversation()?.messages ?? []);
  protected readonly pinned = computed(() => {
    const name = this.conversation()?.skill;
    return name ? (this.catalog()?.skills.find((s) => s.name === name) ?? null) : null;
  });
  protected readonly skillGroups = computed(() => {
    const data = this.catalog();
    return data ? data.stages.map((st) => ({ ...st, skills: data.skills.filter((s) => s.stage_index === st.index) })) : [];
  });
  protected readonly canSend = computed(() => !!this.draft().trim() && !this.chats.busy() && this.settings.ready());

  protected readonly suggestions = [
    'Find recent papers on retrieval augmented generation for question answering',
    'How many participants do I need for a two-group comparison with d = 0.5 and 90% power?',
    'Help me turn my interest in urban heat islands into a research question',
    'I have results and a deadline in three weeks. What do I do next?',
  ];

  constructor() {
    // A link such as /workspace?skill=paper-search&prompt=... opens a fresh chat set up that way.
    effect(() => {
      const skill = this.skill();
      const prompt = this.prompt();
      if (!skill && !prompt) return;
      untracked(() => {
        this.chats.create(skill ?? null);
        if (prompt) this.draft.set(prompt);
        this.router.navigate([], { queryParams: {}, replaceUrl: true });
        this.focusBox();
      });
    });

    // Follow the answer as it streams, unless the reader has scrolled up.
    let lastId: string | null = null;
    effect(() => {
      const conversation = this.conversation();
      this.messages();
      const el = this.scroller()?.nativeElement;
      if (!el) return;
      const switched = conversation?.id !== lastId;
      lastId = conversation?.id ?? null;
      const nearBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 160;
      if (switched || nearBottom) requestAnimationFrame(() => (el.scrollTop = el.scrollHeight));
    });
  }

  protected newChat(): void {
    this.chats.create();
    this.sidebarOpen.set(false);
    this.focusBox();
  }

  protected open(conversation: Conversation): void {
    this.chats.select(conversation.id);
    this.sidebarOpen.set(false);
  }

  protected send(text = this.draft()): void {
    if (!text.trim() || this.chats.busy() || !this.settings.ready()) return;
    this.draft.set('');
    this.resize();
    const el = this.scroller()?.nativeElement;
    if (el) requestAnimationFrame(() => (el.scrollTop = el.scrollHeight));
    void this.chats.send(text);
  }

  protected onKeydown(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey && !event.isComposing) {
      event.preventDefault();
      this.send();
    }
  }

  protected onInput(value: string): void {
    this.draft.set(value);
    this.resize();
  }

  protected pin(name: string): void {
    if (!this.conversation()) this.chats.create(name || null);
    else this.chats.setSkill(name || null);
  }

  protected async addFiles(input: HTMLInputElement): Promise<void> {
    const files = Array.from(input.files ?? []);
    input.value = '';
    this.fileError.set('');
    const room = MAX_FILES - this.chats.activeAttachments().length;
    if (files.length > room) this.fileError.set(`You can attach up to ${MAX_FILES} files per conversation.`);
    const added: Attachment[] = [];
    for (const file of files.slice(0, Math.max(room, 0))) {
      if (file.size > MAX_FILE_BYTES) {
        this.fileError.set(`${file.name} is larger than 3 MB.`);
        continue;
      }
      const name = safeName(file.name);
      if (TEXT_TYPES.test(name)) {
        added.push({ name, content: await file.text(), encoding: 'text', size: file.size });
      } else if (/\.pdf$/i.test(name)) {
        added.push({ name, content: toBase64(await file.arrayBuffer()), encoding: 'base64', size: file.size });
      } else {
        this.fileError.set(`${file.name} is not a supported type. Attach .bib, .csv, .tex, .txt, .md, .json, or .pdf.`);
      }
    }
    if (added.length) this.chats.attach(added);
  }

  protected async copy(message: Message): Promise<void> {
    try {
      await navigator.clipboard.writeText(messageText(message));
      this.copied.set(message.id);
      setTimeout(() => this.copied.set(null), 1600);
    } catch {
      /* clipboard access was refused; nothing to do */
    }
  }

  protected exportChat(): void {
    const conversation = this.conversation();
    if (!conversation) return;
    const body = conversation.messages
      .map((m) => `## ${m.role === 'user' ? 'You' : 'Research Buddy'}\n\n${messageText(m)}`)
      .join('\n\n---\n\n');
    const blob = new Blob([`# ${conversation.title}\n\n${body}\n`], { type: 'text/markdown' });
    const link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = `${conversation.title.replace(/[^\w -]+/g, '').trim().slice(0, 60) || 'conversation'}.md`;
    link.click();
    URL.revokeObjectURL(link.href);
  }

  protected isLast(message: Message): boolean {
    return this.messages().at(-1)?.id === message.id;
  }

  protected kb(bytes: number): string {
    return bytes < 1024 ? `${bytes} B` : bytes < 1_048_576 ? `${Math.round(bytes / 1024)} KB` : `${(bytes / 1_048_576).toFixed(1)} MB`;
  }

  private resize(): void {
    requestAnimationFrame(() => {
      const el = this.textarea()?.nativeElement;
      if (!el) return;
      el.style.height = 'auto';
      el.style.height = `${Math.min(el.scrollHeight, 220)}px`;
    });
  }

  private focusBox(): void {
    requestAnimationFrame(() => {
      this.textarea()?.nativeElement.focus();
      this.resize();
    });
  }
}

/** Reduce a file name to the characters the server accepts. */
function safeName(name: string): string {
  const cleaned = name.normalize('NFKD').replace(/[^A-Za-z0-9._-]+/g, '_').replace(/^[^A-Za-z0-9]+/, '');
  return cleaned.slice(-100) || 'file.txt';
}

function toBase64(buffer: ArrayBuffer): string {
  const bytes = new Uint8Array(buffer);
  let binary = '';
  for (let i = 0; i < bytes.length; i += 0x8000) binary += String.fromCharCode(...bytes.subarray(i, i + 0x8000));
  return btoa(binary);
}
