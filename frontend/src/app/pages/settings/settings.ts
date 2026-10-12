import { ChangeDetectionStrategy, Component, computed, effect, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { ChatStore } from '../../core/chat.store';
import { KeyCheck, Provider } from '../../core/models';
import { SettingsStore, Theme } from '../../core/settings.store';
import { Footer } from '../../shared/footer';
import { Icon } from '../../shared/icon';

@Component({
  selector: 'app-settings',
  imports: [RouterLink, Footer, Icon],
  template: `
    <div class="page-narrow">
      <header class="head">
        <span class="eyebrow">Account on this device</span>
        <h1>Settings</h1>
        <p>
          Keys are sent only as request headers to this site’s API and are never stored on the server.
          Conversations stay in this browser. Scholarly keys also live under
          <a routerLink="/connectors">Connectors</a>.
        </p>
      </header>

      <h2>Model</h2>
      <div class="inset">
        @if (providers(); as list) {
          <div class="field">
            <label for="provider">Provider</label>
            <select
              id="provider"
              [value]="settings.provider()"
              (change)="onProvider($any($event.target).value)"
            >
              @for (p of list; track p.id) {
                <option [value]="p.id">{{ p.name }}</option>
              }
            </select>
          </div>
          @if (current(); as p) {
            <div class="field">
              <label for="model">Model</label>
              <input
                id="model"
                type="text"
                [value]="settings.model()"
                (input)="settings.setModel(p.id, $any($event.target).value)"
                [attr.placeholder]="p.models[0] || 'model id'"
                list="model-suggestions"
                autocomplete="off"
              />
              <datalist id="model-suggestions">
                @for (m of p.models; track m) {
                  <option [value]="m"></option>
                }
              </datalist>
              <span class="hint">Suggestions from {{ p.name }}. Any model id they serve can be typed in.</span>
            </div>
            <div class="field">
              <label for="key">API key</label>
              <div class="key-row">
                <input
                  id="key"
                  [type]="showKey() ? 'text' : 'password'"
                  [value]="settings.apiKey()"
                  (input)="settings.setKey(p.id, $any($event.target).value); check.set(null)"
                  [attr.placeholder]="p.keyHint"
                  autocomplete="off"
                  spellcheck="false"
                />
                <button class="icon-btn" type="button" (click)="showKey.set(!showKey())" [attr.aria-label]="showKey() ? 'Hide key' : 'Show key'">
                  <app-icon [name]="showKey() ? 'check' : 'key'" [size]="16" />
                </button>
              </div>
              <span class="hint">
                <a [href]="p.keyUrl" target="_blank" rel="noopener noreferrer">Get a {{ p.name }} key</a>
              </span>
            </div>
          }
        } @else {
          <p class="field hint">Loading providers…</p>
        }
      </div>
      <div class="row-actions">
        <button
          class="btn"
          type="button"
          [disabled]="!canVerify() || verifying()"
          (click)="verify()"
        >
          {{ verifying() ? 'Verifying…' : 'Verify key' }}
        </button>
        @if (check(); as result) {
          <span class="status" [class.ok]="result.ok" [class.bad]="!result.ok">{{ result.message }}</span>
        }
      </div>

      <h2>Scholarly APIs <span class="optional">optional</span></h2>
      <p class="note">Raise rate limits on Semantic Scholar and PubMed. The skills work without them.</p>
      <div class="inset">
        <div class="field">
          <label for="s2">Semantic Scholar key</label>
          <input
            id="s2"
            type="password"
            [value]="settings.s2Key()"
            (input)="settings.setScholarlyKeys($any($event.target).value, settings.ncbiKey())"
            placeholder="optional"
            autocomplete="off"
          />
        </div>
        <div class="field">
          <label for="ncbi">NCBI / PubMed key</label>
          <input
            id="ncbi"
            type="password"
            [value]="settings.ncbiKey()"
            (input)="settings.setScholarlyKeys(settings.s2Key(), $any($event.target).value)"
            placeholder="optional"
            autocomplete="off"
          />
        </div>
      </div>

      <h2>Appearance</h2>
      <div class="inset theme">
        @for (opt of themes; track opt.id) {
          <button type="button" class="inset-row" [class.on]="settings.theme() === opt.id" (click)="settings.setTheme(opt.id)">
            <app-icon [name]="opt.icon" [size]="16" />
            <span>{{ opt.label }}</span>
            @if (settings.theme() === opt.id) {
              <app-icon name="check" [size]="16" />
            }
          </button>
        }
      </div>

      <h2>Privacy</h2>
      <div class="inset">
        <label class="inset-row">
          <span>
            <strong>Remember keys on this device</strong>
            <em>Off keeps them only until you close the tab.</em>
          </span>
          <span class="switch">
            <input
              type="checkbox"
              [checked]="settings.rememberKeys()"
              (change)="settings.setRememberKeys($any($event.target).checked)"
            />
            <span></span>
          </span>
        </label>
      </div>
      <div class="row-actions">
        <button class="btn btn-ghost" type="button" (click)="clearKeys()">Clear keys</button>
        <button class="btn btn-ghost" type="button" (click)="clearChats()">Delete all conversations</button>
      </div>
      @if (cleared()) {
        <p class="status ok">{{ cleared() }}</p>
      }

      <p class="note jump">Ready? <a routerLink="/workspace">Open the workspace</a>.</p>
      <app-footer />
    </div>
  `,
  styleUrl: './settings.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Settings {
  protected readonly settings = inject(SettingsStore);
  private readonly api = inject(ApiService);
  private readonly chats = inject(ChatStore);

  protected readonly themes: { id: Theme; label: string; icon: string }[] = [
    { id: 'system', label: 'Automatic', icon: 'auto' },
    { id: 'light', label: 'Light', icon: 'sun' },
    { id: 'dark', label: 'Dark', icon: 'moon' },
  ];

  protected readonly showKey = signal(false);
  protected readonly verifying = signal(false);
  protected readonly check = signal<KeyCheck | null>(null);
  protected readonly cleared = signal('');
  protected readonly providers = toSignal(this.api.providers().pipe(catchError(() => of([] as Provider[]))), {
    initialValue: null,
  });
  protected readonly current = computed(() => this.providers()?.find((p) => p.id === this.settings.provider()) ?? null);
  protected readonly canVerify = computed(() => !!this.settings.apiKey() && !!this.settings.model());

  constructor() {
    effect(() => {
      const p = this.current();
      if (p && !this.settings.modelFor(p.id) && p.models[0]) {
        this.settings.setModel(p.id, p.models[0]);
      }
    });
  }

  protected onProvider(id: string): void {
    this.settings.setProvider(id);
    this.check.set(null);
    const p = this.providers()?.find((x) => x.id === id);
    if (p && !this.settings.modelFor(id) && p.models[0]) this.settings.setModel(id, p.models[0]);
  }

  protected verify(): void {
    const p = this.settings.provider();
    const model = this.settings.model();
    const key = this.settings.apiKey();
    if (!model || !key) return;
    this.verifying.set(true);
    this.api.validateKey(p, model, key).subscribe((result) => {
      this.check.set(result);
      this.verifying.set(false);
    });
  }

  protected clearKeys(): void {
    this.settings.clearSecrets();
    this.check.set(null);
    this.cleared.set('Keys removed from this browser.');
  }

  protected clearChats(): void {
    this.chats.clearAll();
    this.cleared.set('All conversations on this device were deleted.');
  }
}
