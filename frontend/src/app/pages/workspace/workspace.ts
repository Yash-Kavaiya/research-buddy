import { DatePipe } from '@angular/common';
import {
  afterNextRender,
  ChangeDetectionStrategy,
  Component,
  ElementRef,
  effect,
  inject,
  signal,
  viewChild,
} from '@angular/core';
import { takeUntilDestroyed, toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { ChatStore } from '../../core/chat.store';
import { Attachment, Message, Thumb, messageText } from '../../core/models';
import { ProjectsStore } from '../../core/projects.store';
import { SettingsStore } from '../../core/settings.store';
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
const MAX_BYTES = 3_000_000;

@Component({
  selector: 'app-workspace',
  imports: [RouterLink, Icon, Markdown, DatePipe],
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
  protected readonly sidebarOpen = signal(false);
  protected readonly expanded = signal<Record<string, boolean>>({});
  protected readonly copied = signal<string | null>(null);
  protected readonly attachError = signal('');
  protected readonly pinnedOpen = signal(false);
  protected readonly raw = signal<Record<string, boolean>>({});
  protected readonly projectName = signal('');
  protected readonly namingProject = signal(false);
  protected readonly notice = signal('');

  private readonly scroller = viewChild<ElementRef<HTMLElement>>('scroller');
  private stickToBottom = true;

  constructor() {
    this.route.queryParamMap.pipe(takeUntilDestroyed()).subscribe((params) => {
      const skill = params.get('skill');
      if (skill) {
        this.chat.create(skill);
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
    el.style.height = 'auto';
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
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
    this.stickToBottom = true;
    await this.chat.send(text);
    this.scrollIfNeeded();
  }

  protected useStarter(text: string): void {
    this.draft.set(text);
  }

  protected newChat(projectId: string | null = null): void {
    this.chat.create(null, projectId);
    this.sidebarOpen.set(false);
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
    this.sidebarOpen.set(false);
  }

  protected setSkill(name: string): void {
    this.chat.setSkill(name || null);
    this.pinnedOpen.set(false);
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
    for (const file of files) {
      if (file.size > MAX_BYTES) {
        this.attachError.set(`${file.name} is larger than 3 MB.`);
        continue;
      }
      if (!/^[A-Za-z0-9._-]+$/.test(file.name)) {
        this.attachError.set(`${file.name} has characters that are not allowed.`);
        continue;
      }
      attachments.push(await readAttachment(file));
    }
    if (attachments.length) this.chat.attach(attachments);
  }

  private scrollIfNeeded(): void {
    const el = this.scroller()?.nativeElement;
    if (el && this.stickToBottom) el.scrollTop = el.scrollHeight;
  }
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
