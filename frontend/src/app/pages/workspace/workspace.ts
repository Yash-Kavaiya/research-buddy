import { DatePipe } from '@angular/common';
import {
  afterNextRender,
  ChangeDetectionStrategy,
  Component,
  computed,
  ElementRef,
  effect,
  inject,
  signal,
  viewChild,
} from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Router } from '@angular/router';
import { catchError, of } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { ChatStore } from '../../core/chat.store';
import { Activity, Attachment, Message, Thumb, messageText } from '../../core/models';
import { ProjectsStore } from '../../core/projects.store';
import { SettingsStore } from '../../core/settings.store';
import { Source, extractSources } from '../../core/sources';
import { UsageStore } from '../../core/usage.store';
import { Icon } from '../../shared/icon';
import { Markdown } from '../../shared/markdown';

const STARTERS = [
  'Find recent papers on retrieval-augmented generation',
  'Turn this interest into a FINER research question: federated learning for medical imaging',
  'How many participants do I need for a two-group t-test with d = 0.5 and power 0.8?',
  'Check whether these citations are real (paste BibTeX or a reference list)',
];

const MAX_FILES = 5;
/**
 * Files are sent base64-encoded inside one JSON request, and Vercel rejects request bodies over
 * 4.5 MB. Keep the total raw size under 2.8 MB (~3.7 MB encoded) to leave room for the chat.
 * Must match MAX_TOTAL_ATTACHMENT_BYTES in api/app/config.py.
 */
export const MAX_TOTAL_BYTES = 2_800_000;

@Component({
  selector: 'app-workspace',
  imports: [Icon, Markdown, DatePipe],
  templateUrl: './workspace.html',
  styleUrl: './workspace.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Workspace {
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  private readonly api = inject(ApiService);
  protected readonly settings = inject(SettingsStore);
  protected readonly chat = inject(ChatStore);
  protected readonly projects = inject(ProjectsStore);
  private readonly usage = inject(UsageStore);

  protected readonly catalog = toSignal(this.api.catalog().pipe(catchError(() => of(null))), {
    initialValue: null,
  });
  protected readonly starters = STARTERS;
  protected readonly draft = signal('');
  /** History column on wide screens; drawers on narrow ones. */
  protected readonly historyOpen = signal(true);
  protected readonly historyDrawer = signal(false);
  protected readonly sourcesDrawer = signal(false);
  protected readonly narrow = mediaSignal('(max-width: 1099px)');
  private readonly wide = mediaSignal('(min-width: 1280px)');
  protected readonly tabs = signal<Record<string, Tab>>({});
  /** The answer whose sources the rail shows; null follows the latest answer. */
  protected readonly focusId = signal<string | null>(null);
  protected readonly activeCite = signal<number | null>(null);
  protected readonly skillQuery = signal('');
  protected readonly expanded = signal<Record<string, boolean>>({});
  protected readonly copied = signal<string | null>(null);
  protected readonly attachError = signal('');
  protected readonly pinnedOpen = signal(false);
  protected readonly raw = signal<Record<string, boolean>>({});
  protected readonly projectName = signal('');
  protected readonly namingProject = signal(false);
  protected readonly notice = signal('');

  private readonly scroller = viewChild<ElementRef<HTMLElement>>('scroller');
  private readonly box = viewChild<ElementRef<HTMLTextAreaElement>>('box');
  private stickToBottom = true;

  /** Sources per assistant message, recomputed as answers stream in. */
  private readonly sources = computed(() => {
    const map: Record<string, Source[]> = {};
    for (const m of this.chat.active()?.messages ?? []) {
      if (m.role === 'assistant') map[m.id] = extractSources(messageText(m));
    }
    return map;
  });

  protected readonly hasMessages = computed(() => !!this.chat.active()?.messages.length);

  protected readonly focusMessage = computed<Message | null>(() => {
    const messages = this.chat.active()?.messages ?? [];
    const id = this.focusId();
    const chosen = id ? messages.find((m) => m.id === id) : undefined;
    return chosen ?? [...messages].reverse().find((m) => m.role === 'assistant') ?? null;
  });

  protected readonly focusSources = computed(() => {
    const m = this.focusMessage();
    return m ? (this.sources()[m.id] ?? []) : [];
  });

  protected readonly skillMatches = computed(() => {
    const q = this.skillQuery().trim().toLowerCase();
    const skills = this.catalog()?.skills ?? [];
    return q ? skills.filter((s) => s.name.includes(q) || s.description.toLowerCase().includes(q)) : skills;
  });

  protected readonly shortModel = computed(() => {
    const model = this.settings.model();
    if (!model) return 'Choose model';
    const name = model.split('/').pop() ?? model;
    return name.length > 22 ? name.slice(0, 21) + '…' : name;
  });

  constructor() {
    this.route.queryParamMap.pipe(takeUntilDestroyed()).subscribe((params) => {
      const skill = params.get('skill');
      const question = params.get('q');
      if (skill || question) {
        if (skill || this.chat.active()?.messages.length) this.chat.create(skill);
        else if (!this.chat.active()) this.chat.create();
        if (question) this.useStarter(question.slice(0, 4000));
        void this.router.navigate(['/workspace'], { replaceUrl: true });
        return;
      }
      if (!this.chat.active()) this.chat.create();
    });
    afterNextRender(() => this.scrollIfNeeded());
    effect(() => {
      this.chat.active()?.messages.length;
      this.chat.busy();
      queueMicrotask(() => this.scrollIfNeeded());
    });
  }

  protected onScroll(event: Event): void {
    const el = event.target as HTMLElement;
    this.stickToBottom = el.scrollHeight - el.scrollTop - el.clientHeight < 80;
  }

  protected onDraft(event: Event): void {
    const el = event.target as HTMLTextAreaElement;
    this.draft.set(el.value);
    this.fitBox(el);
  }

  private fitBox(el: HTMLTextAreaElement): void {
    el.style.height = 'auto';
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  }

  private resetBox(): void {
    const el = this.box()?.nativeElement;
    if (el) el.style.height = 'auto';
  }

  protected onEnter(event: Event): void {
    const ke = event as KeyboardEvent;
    if (ke.key === 'Enter' && !ke.shiftKey) {
      ke.preventDefault();
      void this.submit();
    }
  }

  protected async submit(): Promise<void> {
    const text = this.draft().trim();
    if (!text) return;
    this.draft.set('');
    this.resetBox();
    this.stickToBottom = true;
    this.focusId.set(null);
    this.activeCite.set(null);
    await this.chat.send(text);
    this.scrollIfNeeded();
  }

  protected useStarter(text: string): void {
    this.draft.set(text);
    queueMicrotask(() => {
      const box = this.box()?.nativeElement;
      if (!box) return;
      box.focus();
      this.fitBox(box);
    });
  }

  protected newChat(projectId: string | null = null): void {
    this.chat.create(null, projectId);
    this.historyDrawer.set(false);
    this.focusId.set(null);
  }

  protected openHistory(): void {
    if (this.narrow()) this.historyDrawer.set(true);
    else this.historyOpen.set(true);
  }

  protected closeHistory(): void {
    if (this.narrow()) this.historyDrawer.set(false);
    else this.historyOpen.set(false);
  }

  protected closeDrawers(): void {
    this.historyDrawer.set(false);
    this.sourcesDrawer.set(false);
  }

  protected goSettings(): void {
    void this.router.navigate(['/settings']);
  }

  protected tabOf(id: string): Tab {
    return this.tabs()[id] ?? 'answer';
  }

  protected setTab(id: string, tab: Tab): void {
    this.tabs.update((t) => ({ ...t, [id]: tab }));
    this.focusId.set(id);
  }

  protected sourcesOf(id: string): Source[] {
    return this.sources()[id] ?? [];
  }

  protected stepsOf(message: Message): Activity[] {
    return message.blocks.filter((b): b is Activity => b.type === 'activity');
  }

  protected hasText(message: Message): boolean {
    return message.blocks.some((b) => b.type === 'text' && b.text.trim());
  }

  /** A citation chip was clicked: show and highlight its source card. */
  protected onCite(messageId: string, n: number): void {
    this.focusId.set(messageId);
    this.activeCite.set(n);
    if (!this.wide()) this.sourcesDrawer.set(true);
    setTimeout(() => document.getElementById(`src-${n}`)?.scrollIntoView({ block: 'nearest', behavior: 'smooth' }), 30);
  }

  protected chatsIn(projectId: string | null) {
    return this.chat.conversations().filter((c) => (c.projectId ?? null) === projectId);
  }

  protected addProject(): void {
    const project = this.projects.create(this.projectName());
    this.projectName.set('');
    this.namingProject.set(false);
    if (project) this.chat.create(this.chat.active()?.skill ?? null, project.id);
  }

  protected deleteProject(id: string): void {
    this.projects.remove(id);
    this.chat.releaseProject(id);
  }

  protected selectChat(id: string): void {
    this.chat.select(id);
    this.historyDrawer.set(false);
    this.focusId.set(null);
    this.activeCite.set(null);
  }

  protected setSkill(name: string): void {
    this.chat.setSkill(name || null);
    this.pinnedOpen.set(false);
    this.skillQuery.set('');
  }

  protected toggleActivity(id: string): void {
    this.expanded.update((m) => ({ ...m, [id]: !m[id] }));
  }

  protected async copy(id: string, text: string, label = 'copy'): Promise<void> {
    try {
      await navigator.clipboard.writeText(text);
      this.copied.set(`${label}:${id}`);
      setTimeout(() => this.copied.update((c) => (c === `${label}:${id}` ? null : c)), 1600);
    } catch {
      this.notice.set('Could not copy.');
    }
  }

  protected toggleMarkdown(id: string): void {
    this.raw.update((m) => ({ ...m, [id]: !m[id] }));
  }

  protected async share(message: Message): Promise<void> {
    const text = messageText(message);
    const title = this.chat.active()?.title ?? 'Research Buddy';
    try {
      if (navigator.share) {
        await navigator.share({ title, text });
        this.notice.set('Shared.');
        return;
      }
      await this.copy(message.id, `# ${title}\n\n${text}`, 'share');
      this.notice.set('Markdown copied to share.');
    } catch {
      this.notice.set('Share was cancelled.');
    }
  }

  protected branch(id: string): void {
    const next = this.chat.branchAt(id);
    if (next) this.notice.set('Branched into a new chat.');
  }

  protected rate(id: string, thumb: Thumb): void {
    this.chat.rateMessage(id, thumb);
    this.usage.submit(thumb, '', 'message');
    this.api.feedback(thumb, '', 'message').subscribe({ error: () => undefined });
  }

  protected messagePlain(id: string): string {
    const msg = this.chat.active()?.messages.find((m) => m.id === id);
    return msg ? messageText(msg) : '';
  }

  protected needsSettings(error?: string): boolean {
    const t = (error ?? '').toLowerCase();
    return t.includes('api key') || t.includes('settings') || t.includes('unauthorized');
  }

  protected async onFiles(event: Event): Promise<void> {
    const input = event.target as HTMLInputElement;
    const files = Array.from(input.files ?? []);
    input.value = '';
    this.attachError.set('');
    const existing = this.chat.activeAttachments().length;
    if (existing + files.length > MAX_FILES) {
      this.attachError.set(`Up to ${MAX_FILES} files per chat.`);
      return;
    }
    const attachments: Attachment[] = [];
    let total = this.chat.activeAttachments().reduce((sum, a) => sum + attachmentBytes(a), 0);
    for (const file of files) {
      if (total + file.size > MAX_TOTAL_BYTES) {
        this.attachError.set(
          `${file.name} would take attachments over ${MAX_TOTAL_BYTES / 1_000_000} MB in total.`,
        );
        continue;
      }
      if (!/^[A-Za-z0-9._-]+$/.test(file.name)) {
        this.attachError.set(`${file.name} has characters that are not allowed.`);
        continue;
      }
      attachments.push(await readAttachment(file));
      total += file.size;
    }
    if (attachments.length) this.chat.attach(attachments);
  }

  private scrollIfNeeded(): void {
    const el = this.scroller()?.nativeElement;
    if (el && this.stickToBottom) el.scrollTop = el.scrollHeight;
  }
}

type Tab = 'answer' | 'sources' | 'steps';

/** A signal that tracks a CSS media query. */
function mediaSignal(query: string) {
  const mql = typeof matchMedia === 'function' ? matchMedia(query) : null;
  const value = signal(mql?.matches ?? false);
  mql?.addEventListener('change', (e) => value.set(e.matches));
  return value.asReadonly();
}

/** Approximate raw size of an attachment already read into memory. */
export function attachmentBytes(a: Attachment): number {
  if (a.encoding === 'base64') return Math.floor((a.content.length * 3) / 4);
  return new TextEncoder().encode(a.content).length;
}

function readAttachment(file: File): Promise<Attachment> {
  const textual =
    /^text\/|json|csv|xml|markdown|latex/.test(file.type) ||
    /\.(txt|md|csv|json|bib|tex|py|html|xml|tsv)$/i.test(file.name);
  if (textual) {
    return file.text().then((content) => ({ name: file.name, content, encoding: 'text' as const }));
  }
  return new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onerror = () => reject(reader.error);
    reader.onload = () => {
      const result = String(reader.result ?? '');
      const base64 = result.includes(',') ? result.slice(result.indexOf(',') + 1) : result;
      resolve({ name: file.name, content: base64, encoding: 'base64' });
    };
    reader.readAsDataURL(file);
  });
}
