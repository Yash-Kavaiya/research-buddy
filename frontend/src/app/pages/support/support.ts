import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';

import { ApiService } from '../../core/api.service';
import { Thumb } from '../../core/models';
import { UsageStore, githubIssueUrl } from '../../core/usage.store';
import { Footer } from '../../shared/footer';
import { Icon } from '../../shared/icon';

@Component({
  selector: 'app-support',
  imports: [Footer, Icon],
  template: `
    <div class="page-narrow">
      <header class="head">
        <span class="eyebrow">Project</span>
        <h1>Support this project</h1>
        <p>
          Research Buddy is free to run because you bring your own model key. Stars, shares, and written reviews are
          what keep the skill library moving.
        </p>
      </header>

      <div class="actions">
        <a class="btn" href="https://github.com/Yash-Kavaiya/research-buddy" target="_blank" rel="noopener noreferrer">
          Star on GitHub
        </a>
        <a
          class="btn btn-ghost"
          href="https://github.com/Yash-Kavaiya/research-scholar-agent-skills"
          target="_blank"
          rel="noopener noreferrer"
        >
          Skill library
        </a>
        <button class="btn btn-ghost" type="button" (click)="share()">Share</button>
      </div>
      @if (shared()) {
        <p class="status">{{ shared() }}</p>
      }

      <h2>Feedback review</h2>
      <div class="inset">
        <div class="field">
          <span class="label">Rating</span>
          <div class="thumbs">
            <button type="button" [class.on]="kind() === 'up'" (click)="kind.set('up')">
              <app-icon name="up" [size]="16" /> Up
            </button>
            <button type="button" [class.on]="kind() === 'down'" (click)="kind.set('down')">
              <app-icon name="down" [size]="16" /> Down
            </button>
            <button type="button" [class.on]="kind() === 'review'" (click)="kind.set('review')">Written review</button>
          </div>
        </div>
        <div class="field">
          <label for="review">Review</label>
          <textarea
            id="review"
            rows="5"
            [value]="message()"
            (input)="message.set($any($event.target).value)"
            maxlength="4000"
            placeholder="What should the next version do better?"
          ></textarea>
        </div>
      </div>
      <div class="row">
        <button class="btn" type="button" [disabled]="!message().trim() && kind() === 'review'" (click)="save()">
          Save review
        </button>
        <button class="btn btn-ghost" type="button" (click)="openIssue()">Open as GitHub issue</button>
      </div>
      @if (saved()) {
        <p class="status">{{ saved() }}</p>
      }

      @if (usage.reviews().length) {
        <h2>Reviews on this device</h2>
        <ul class="reviews">
          @for (r of usage.reviews(); track r.id) {
            <li class="inset">
              <strong>{{ r.kind }}</strong>
              <span>{{ r.source }}</span>
              @if (r.message) {
                <p>{{ r.message }}</p>
              }
            </li>
          }
        </ul>
      }

      <p class="fineprint">
        Reviews are kept in this browser. Saving one also tells the API it arrived; the server does not store the text.
        Research Buddy can make mistakes. Check citations and numbers before you rely on them.
      </p>
      <app-footer />
    </div>
  `,
  styles: `
    .head {
      margin-bottom: 22px;
      h1 {
        font-size: 40px;
        margin-bottom: 8px;
      }
    }
    .actions,
    .row,
    .thumbs {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
    }
    .row {
      margin-top: 14px;
    }
    h2 {
      margin: 32px 0 10px;
      font-size: 20px;
    }
    textarea {
      width: 100%;
      border: 0;
      background: transparent;
      resize: vertical;
      outline: none;
    }
    .label {
      font-size: 13px;
      color: var(--text-2);
    }
    .thumbs button {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      padding: 6px 12px;
      border: 1px solid var(--border);
      border-radius: var(--radius-pill);
      background: transparent;
      font-size: 14px;
      &.on {
        border-color: var(--accent);
        background: var(--accent-soft);
      }
    }
    .status {
      margin-top: 10px;
      color: var(--success);
      font-size: 14px;
    }
    .reviews {
      list-style: none;
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      gap: 8px;
      li {
        padding: 12px 16px;
      }
      strong {
        text-transform: capitalize;
        margin-right: 8px;
      }
      span {
        color: var(--text-3);
        font-size: 12px;
      }
      p {
        margin-top: 6px;
        font-size: 14px;
        color: var(--text);
      }
    }
    .fineprint {
      margin-top: 28px;
      font-size: 11px;
      line-height: 1.4;
      color: var(--text-3);
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Support {
  private readonly api = inject(ApiService);
  protected readonly usage = inject(UsageStore);
  protected readonly kind = signal<Thumb | 'review'>('review');
  protected readonly message = signal('');
  protected readonly saved = signal('');
  protected readonly shared = signal('');

  protected save(): void {
    const kind = this.kind();
    const message = this.message().trim();
    if (kind === 'review' && !message) return;
    this.usage.submit(kind, message, 'support');
    this.api.feedback(kind, message, 'support').subscribe({
      next: (r) => this.saved.set(r.message),
      error: () => this.saved.set('Saved on this device. The server could not be reached.'),
    });
    this.message.set('');
  }

  protected openIssue(): void {
    const body = `${this.kind()}\n\n${this.message().trim()}`.trim();
    window.open(githubIssueUrl('Research Buddy feedback', body), '_blank', 'noopener,noreferrer');
  }

  protected async share(): Promise<void> {
    const data = {
      title: 'Research Buddy',
      text: 'Research assistant that runs real research skills. Bring your own model key.',
      url: 'https://github.com/Yash-Kavaiya/research-buddy',
    };
    try {
      if (navigator.share) {
        await navigator.share(data);
        this.shared.set('Thanks for sharing.');
        return;
      }
      await navigator.clipboard.writeText(data.url);
      this.shared.set('Project link copied.');
    } catch {
      this.shared.set('Share was cancelled.');
    }
  }
}
