import { ChangeDetectionStrategy, Component, computed, inject, input } from '@angular/core';
import { toObservable, toSignal } from '@angular/core/rxjs-interop';
import { Title } from '@angular/platform-browser';
import { RouterLink } from '@angular/router';
import { catchError, map, of, startWith, switchMap, tap } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { SkillDetail } from '../../core/models';
import { Footer } from '../../shared/footer';
import { Icon } from '../../shared/icon';
import { Markdown } from '../../shared/markdown';

type State = { status: 'loading' } | { status: 'missing' } | { status: 'ready'; skill: SkillDetail };

@Component({
  selector: 'app-skill-detail',
  imports: [RouterLink, Icon, Markdown, Footer],
  template: `
    <article class="container page">
      <a class="back" routerLink="/skills"><app-icon name="chevron" [size]="14" /> Skills</a>

      @switch (state().status) {
        @case ('loading') {
          <div class="page-state"><span class="spinner"></span>Loading</div>
        }
        @case ('missing') {
          <div class="page-state">
            <p>This skill could not be found.</p>
            <a class="btn small" routerLink="/skills">See all skills</a>
          </div>
        }
        @case ('ready') {
          @let skill = ready()!;
          <header class="head" [style.--stage]="'var(--stage-' + skill.stage_index + ')'">
            <a class="stage" routerLink="/skills" [queryParams]="{ stage: skill.stage_index }">
              <span class="stage-dot"></span>{{ skill.stage }}
            </a>
            <h1 class="headline">{{ skill.title }}</h1>
            <p class="lead">{{ skill.summary }}.</p>
            <div class="actions">
              <a class="btn" routerLink="/workspace" [queryParams]="{ skill: skill.name }">Use this skill</a>
              <span class="caption mono">{{ skill.name }}</span>
            </div>
          </header>

          <div class="layout">
            <app-markdown class="doc" [source]="body()" />
            <aside>
              @if (skill.scripts.length) {
                <section>
                  <h2>Scripts</h2>
                  <p class="caption">The agent runs these for you and shows the output.</p>
                  <ul>
                    @for (script of skill.scripts; track script) {
                      <li class="mono"><app-icon name="terminal" [size]="14" /> {{ script }}</li>
                    }
                  </ul>
                </section>
              }
              @if (skill.references.length) {
                <section>
                  <h2>Reference files</h2>
                  <ul>
                    @for (file of skill.references; track file) {
                      <li class="mono"><app-icon name="doc" [size]="14" /> {{ file }}</li>
                    }
                  </ul>
                </section>
              }
              @if (skill.tags.length) {
                <section>
                  <h2>Tags</h2>
                  <div class="tags">
                    @for (tag of skill.tags; track tag) {
                      <span class="chip">{{ tag }}</span>
                    }
                  </div>
                </section>
              }
            </aside>
          </div>
        }
      }
    </article>
    <app-footer />
  `,
  styles: `
    :host {
      display: flex;
      flex-direction: column;
      flex: 1;
    }

    .page {
      padding-top: 28px;
      padding-bottom: clamp(56px, 8vw, 96px);
    }

    .back {
      display: inline-flex;
      align-items: center;
      gap: 2px;
      font-size: 14px;

      app-icon {
        transform: rotate(180deg);
      }
    }

    .head {
      display: grid;
      justify-items: start;
      gap: 12px;
      max-width: 760px;
      padding: clamp(24px, 4vw, 44px) 0 clamp(28px, 4vw, 44px);
    }

    .stage {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      color: var(--text-2);
      font-size: 14px;
      font-weight: 600;
    }

    .actions {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 12px 18px;
      margin-top: 8px;
    }

    .layout {
      display: grid;
      grid-template-columns: minmax(0, 1fr) 280px;
      gap: clamp(28px, 5vw, 64px);
      align-items: start;
      padding-top: clamp(24px, 4vw, 40px);
      border-top: 1px solid var(--border);
    }

    aside {
      position: sticky;
      top: calc(var(--nav-height) + 24px);
      display: grid;
      gap: 26px;

      h2 {
        margin-bottom: 8px;
        font-size: 14px;
        letter-spacing: -0.01em;
      }

      ul {
        display: grid;
        gap: 8px;
        margin: 10px 0 0;
        padding: 0;
        list-style: none;
      }

      li {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 12.5px;
        color: var(--text-2);
        overflow-wrap: anywhere;
      }
    }

    .tags {
      display: flex;
      flex-wrap: wrap;
      gap: 6px;
    }

    @media (max-width: 860px) {
      .layout {
        grid-template-columns: minmax(0, 1fr);
      }

      aside {
        position: static;
        order: -1;
        padding: 20px;
        border-radius: var(--radius-l);
        background: var(--bg-alt);
      }
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SkillDetailPage {
  private readonly api = inject(ApiService);
  private readonly title = inject(Title);

  /** Bound from the :name route parameter. */
  readonly name = input.required<string>();

  protected readonly state = toSignal(
    toObservable(this.name).pipe(
      switchMap((name) =>
        this.api.skill(name).pipe(
          tap((skill) => this.title.setTitle(`${skill.title} · Research Buddy`)),
          map((skill): State => ({ status: 'ready', skill })),
          catchError(() => of<State>({ status: 'missing' })),
          startWith<State>({ status: 'loading' }),
        ),
      ),
    ),
    { initialValue: { status: 'loading' } as State },
  );

  protected readonly ready = computed(() => {
    const state = this.state();
    return state.status === 'ready' ? state.skill : null;
  });

  /** The page header already shows the title, so drop the document's own first heading. */
  protected readonly body = computed(() => (this.ready()?.markdown ?? '').replace(/^\s*#\s+.+\n+/, ''));
}
