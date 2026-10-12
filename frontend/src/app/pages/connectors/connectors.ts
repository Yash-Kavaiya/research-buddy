import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { catchError, of } from 'rxjs';

import { ApiService, Connector } from '../../core/api.service';
import { SettingsStore } from '../../core/settings.store';
import { Footer } from '../../shared/footer';

@Component({
  selector: 'app-connectors',
  imports: [Footer],
  template: `
    <div class="page-narrow">
      <header class="head">
        <span class="eyebrow">Sources</span>
        <h1>Connectors</h1>
        <p>
          Literature scripts already talk to arXiv and Crossref. Add a key or a contact email when you want a higher
          rate limit. Values stay in this browser and go out only as request headers.
        </p>
      </header>

      @if (connectors(); as list) {
        <div class="stack">
          @for (c of list; track c.id) {
            <article class="inset">
              <div class="field">
                <div class="title">
                  <strong>{{ c.name }}</strong>
                  <span class="pill">{{ status(c) }}</span>
                </div>
                <p>{{ c.detail }}</p>
                @if (c.kind === 'key' && c.id === 's2') {
                  <input
                    type="password"
                    [value]="settings.s2Key()"
                    (input)="settings.setScholarlyKeys($any($event.target).value, settings.ncbiKey())"
                    placeholder="Semantic Scholar API key"
                    autocomplete="off"
                  />
                }
                @if (c.kind === 'key' && c.id === 'ncbi') {
                  <input
                    type="password"
                    [value]="settings.ncbiKey()"
                    (input)="settings.setScholarlyKeys(settings.s2Key(), $any($event.target).value)"
                    placeholder="NCBI API key"
                    autocomplete="off"
                  />
                }
                @if (c.kind === 'email') {
                  <input
                    type="email"
                    [value]="settings.openAlexEmail()"
                    (input)="settings.setOpenAlexEmail($any($event.target).value)"
                    placeholder="you@university.edu"
                    autocomplete="email"
                  />
                }
                @if (c.keyUrl) {
                  <a class="hint" [href]="c.keyUrl" target="_blank" rel="noopener noreferrer">Get a key</a>
                }
              </div>
            </article>
          }
        </div>
      } @else {
        <p class="banner banner-warn">Could not load connectors. Is the API running?</p>
      }
      <app-footer />
    </div>
  `,
  styles: `
    .head {
      margin-bottom: 28px;
      h1 {
        font-size: 40px;
        margin-bottom: 8px;
      }
    }
    .stack {
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .title {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 8px;
    }
    .field p {
      margin: 6px 0 0;
      font-size: 14px;
    }
    input {
      margin-top: 10px;
      width: 100%;
      padding: 8px 0;
      border: 0;
      border-bottom: 1px solid var(--border);
      background: transparent;
      outline: none;
    }
    .hint {
      display: inline-block;
      margin-top: 8px;
      font-size: 13px;
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Connectors {
  private readonly api = inject(ApiService);
  protected readonly settings = inject(SettingsStore);
  protected readonly connectors = toSignal(this.api.connectors().pipe(catchError(() => of(null as Connector[] | null))));

  protected status(connector: Connector): string {
    if (connector.kind === 'builtin') return 'Built in';
    if (connector.id === 's2') return this.settings.s2Key() ? 'Connected' : 'Off';
    if (connector.id === 'ncbi') return this.settings.ncbiKey() ? 'Connected' : 'Off';
    if (connector.id === 'openalex') return this.settings.openAlexEmail() ? 'Connected' : 'Off';
    return 'Off';
  }
}
