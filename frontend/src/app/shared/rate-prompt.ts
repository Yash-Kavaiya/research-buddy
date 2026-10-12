import { HttpClient } from '@angular/common/http';
import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';

import { Thumb } from '../core/models';
import { UsageStore } from '../core/usage.store';
import { Icon } from './icon';

@Component({
  selector: 'app-rate-prompt',
  imports: [Icon],
  template: `
    @if (usage.promptOpen()) {
      <div class="backdrop" role="presentation" (click)="usage.later()">
        <div class="sheet" role="dialog" aria-modal="true" aria-labelledby="rate-title" (click)="$event.stopPropagation()">
          <h2 id="rate-title">How are the first chats?</h2>
          <p>You’ve used five free chats. A thumbs up or down helps the project. It stays on this device.</p>
          <div class="thumbs">
            <button type="button" [class.on]="choice() === 'up'" (click)="choice.set('up')" aria-label="Thumbs up">
              <app-icon name="up" [size]="18" />
              Up
            </button>
            <button type="button" [class.on]="choice() === 'down'" (click)="choice.set('down')" aria-label="Thumbs down">
              <app-icon name="down" [size]="18" />
              Down
            </button>
          </div>
          <label class="note">
            Optional note
            <textarea rows="3" [value]="note()" (input)="note.set($any($event.target).value)" maxlength="1000"></textarea>
          </label>
          <div class="actions">
            <button class="btn btn-ghost" type="button" (click)="usage.later()">Later</button>
            <button class="btn" type="button" [disabled]="!choice()" (click)="send()">Rate</button>
          </div>
        </div>
      </div>
    }
  `,
  styles: `
    .backdrop {
      position: fixed;
      inset: 0;
      z-index: 80;
      display: grid;
      place-items: center;
      padding: 20px;
      background: rgba(0, 0, 0, 0.45);
    }

    .sheet {
      width: min(420px, 100%);
      padding: 22px;
      border-radius: var(--radius-l);
      background: var(--bg-elevated);
      box-shadow: var(--shadow-raised);
    }

    h2 {
      font-size: 22px;
      margin-bottom: 8px;
    }

    p {
      font-size: 14px;
    }

    .thumbs {
      display: flex;
      gap: 8px;
      margin: 16px 0;
    }

    .thumbs button {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 8px 14px;
      border: 1px solid var(--border);
      border-radius: var(--radius-pill);
      background: transparent;

      &.on {
        border-color: var(--accent);
        background: var(--accent-soft);
      }
    }

    .note {
      display: flex;
      flex-direction: column;
      gap: 6px;
      font-size: 13px;
      color: var(--text-2);

      textarea {
        border: 1px solid var(--border);
        border-radius: var(--radius-m);
        background: var(--bg);
        padding: 8px 10px;
        resize: vertical;
      }
    }

    .actions {
      display: flex;
      justify-content: flex-end;
      gap: 8px;
      margin-top: 16px;
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class RatePrompt {
  protected readonly usage = inject(UsageStore);
  private readonly http = inject(HttpClient);
  protected readonly choice = signal<Thumb | null>(null);
  protected readonly note = signal('');

  protected send(): void {
    const kind = this.choice();
    if (!kind) return;
    const message = this.note();
    this.usage.submit(kind, message, 'popup');
    this.http.post('/api/feedback', { kind, message, source: 'popup' }).subscribe({ error: () => undefined });
  }
}
