import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, Router, RouterLink } from '@angular/router';
import { catchError, of, switchMap } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { Footer } from '../../shared/footer';
import { Icon } from '../../shared/icon';
import { Markdown } from '../../shared/markdown';

@Component({
  selector: 'app-skill-detail',
  imports: [RouterLink, Footer, Markdown, Icon],
  template: `
    <div class="page">
      @if (skill(); as s) {
        <button class="back" type="button" (click)="back()">
          <app-icon name="chevron" [size]="14" class="flip" /> Library
        </button>
        <div class="layout">
          <article class="main">
            <span class="eyebrow">{{ s.stageName }}</span>
            <h1 class="mono-title">{{ s.name }}</h1>
            <p class="lede">{{ s.description }}</p>
            <div class="doc">
              <app-markdown [source]="s.body" />
            </div>
          </article>

          <aside class="side">
            <div class="panel">
              <button class="btn use" type="button" (click)="use(s.name)">
                <app-icon name="spark" [size]="16" /> Use this skill
              </button>
              <dl>
                <div>
                  <dt>Stage</dt>
                  <dd>
                    <i class="dot" [style.background]="'var(--stage-' + s.stageNumber + ')'"></i>
                    {{ s.stageName }}
                  </dd>
                </div>
                @if (s.scripts.length) {
                  <div>
                    <dt>Scripts</dt>
                    <dd class="scripts">
                      @for (f of s.scripts; track f) {
                        <span class="mono"><app-icon name="terminal" [size]="13" /> {{ f }}</span>
                      }
                    </dd>
                  </div>
                } @else {
                  <div>
                    <dt>Scripts</dt>
                    <dd class="muted">Guidance only</dd>
                  </div>
                }
                @if (s.tags.length) {
                  <div>
                    <dt>Tags</dt>
                    <dd class="tags">
                      @for (t of s.tags; track t) {
                        <span class="pill">{{ t }}</span>
                      }
                    </dd>
                  </div>
                }
                @if (s.compatibility) {
                  <div>
                    <dt>Needs</dt>
                    <dd class="muted">{{ s.compatibility }}</dd>
                  </div>
                }
              </dl>
            </div>
          </aside>
        </div>
      } @else if (skill() === null) {
        <div class="missing">
          <h1>Skill not found</h1>
          <p><a routerLink="/skills">Back to the library</a></p>
        </div>
      }
      <app-footer />
    </div>
  `,
  styles: `
    .back {
      display: inline-flex;
      align-items: center;
      gap: 4px;
      margin-bottom: 24px;
      padding: 6px 12px 6px 8px;
      border: 1px solid var(--border);
      border-radius: var(--radius-pill);
      background: var(--bg-elevated);
      color: var(--text-2);
      font-size: 13px;
      font-weight: 500;

      &:hover {
        color: var(--text);
      }

      .flip {
        transform: rotate(180deg);
      }
    }

    .layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 300px;
      gap: 40px;
      align-items: start;
    }

    .mono-title {
      margin-bottom: 12px;
      font-family: var(--font-mono);
      font-size: clamp(24px, 3.6vw, 34px);
      font-weight: 600;
      letter-spacing: -0.02em;
      overflow-wrap: anywhere;
    }

    .lede {
      margin-bottom: 28px;
      font-size: 17px;
      line-height: 1.6;
    }

    .doc {
      padding: 28px 32px;
      border: 1px solid var(--border);
      border-radius: var(--radius-l);
      background: var(--bg-elevated);
      box-shadow: var(--shadow-card);
    }

    .side {
      position: sticky;
      top: calc(var(--chrome-top, 0px) + 24px);
    }

    .panel {
      display: grid;
      gap: 18px;
      padding: 20px;
      border: 1px solid var(--border);
      border-radius: var(--radius-l);
      background: var(--bg-elevated);
      box-shadow: var(--shadow-card);
    }

    .use {
      width: 100%;
      min-height: 44px;
    }

    dl {
      display: grid;
      gap: 16px;
      margin: 0;
    }

    dt {
      margin-bottom: 6px;
      color: var(--text-3);
      font-size: 11px;
      font-weight: 600;
      letter-spacing: 0.1em;
      text-transform: uppercase;
    }

    dd {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 6px;
      margin: 0;
      color: var(--text);
      font-size: 14px;
    }

    .dot {
      width: 8px;
      height: 8px;
      border-radius: 50%;
    }

    .scripts {
      display: grid;
      gap: 6px;

      span {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 6px 10px;
        border-radius: var(--radius-s);
        background: var(--bg-inset);
        font-size: 12px;
        overflow-wrap: anywhere;
      }
    }

    .muted {
      color: var(--text-2);
      font-size: 13.5px;
    }

    .missing {
      padding: 40px 0;
    }

    @media (max-width: 960px) {
      .layout {
        grid-template-columns: minmax(0, 1fr);
        gap: 24px;
      }

      .side {
        position: static;
        order: -1;
      }
    }

    @media (max-width: 640px) {
      .doc {
        padding: 20px 18px;
      }
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SkillDetailPage {
  private readonly api = inject(ApiService);
  private readonly route = inject(ActivatedRoute);
  private readonly router = inject(Router);
  protected readonly skill = toSignal(
    this.route.paramMap.pipe(
      switchMap((params) => this.api.skill(params.get('name') ?? '').pipe(catchError(() => of(null)))),
    ),
  );

  protected use(name: string): void {
    void this.router.navigate(['/workspace'], { queryParams: { skill: name } });
  }

  protected back(): void {
    void this.router.navigate(['/skills']);
  }
}
