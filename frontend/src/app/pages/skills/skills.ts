import { ChangeDetectionStrategy, Component, computed, inject, input, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { SkillBrief } from '../../core/models';
import { Footer } from '../../shared/footer';
import { Icon } from '../../shared/icon';

@Component({
  selector: 'app-skills',
  imports: [RouterLink, Icon, Footer],
  template: `
    <section class="container head">
      <h1 class="headline">Skills</h1>
      <p class="lead">59 skills across the research lifecycle. Open one to read its method, or start a chat with it.</p>

      <label class="search">
        <span class="sr-only">Search skills</span>
        <app-icon name="search" [size]="18" />
        <input
          type="search"
          placeholder="Search by name, task, or tag"
          autocomplete="off"
          [value]="query()"
          (input)="query.set($any($event.target).value)"
        />
      </label>

      @if (catalog(); as data) {
        <div class="filters" role="group" aria-label="Filter by stage">
          <button class="chip" type="button" [attr.aria-pressed]="!activeStage()" (click)="setStage(null)">All</button>
          @for (stage of data.stages; track stage.index) {
            <button
              class="chip"
              type="button"
              [attr.aria-pressed]="activeStage() === stage.index"
              (click)="setStage(stage.index)"
            >
              {{ stage.name }}
            </button>
          }
        </div>
      }
    </section>

    <section class="container body" aria-live="polite">
      @if (catalog() === undefined) {
        <div class="page-state"><span class="spinner"></span>Loading skills</div>
      } @else if (catalog() === null) {
        <div class="page-state">
          <p>The skill catalog could not be loaded.</p>
          <button class="btn small" type="button" (click)="reload()">Try again</button>
        </div>
      } @else {
        @for (group of groups(); track group.index) {
          <section class="group" [style.--stage]="'var(--stage-' + group.index + ')'">
            <h2><span class="stage-dot"></span>{{ group.name }} <span class="count">{{ group.skills.length }}</span></h2>
            <ul>
              @for (skill of group.skills; track skill.name) {
                <li>
                  <a class="skill card" [routerLink]="['/skills', skill.name]">
                    <h3>{{ skill.title }}</h3>
                    <p>{{ skill.summary }}</p>
                    @if (skill.scripts.length) {
                      <span class="chip"><app-icon name="terminal" [size]="13" /> Runs a script</span>
                    }
                  </a>
                </li>
              }
            </ul>
          </section>
        } @empty {
          <div class="page-state">
            <p>No skill matches “{{ query() }}”.</p>
            <button class="btn small quiet" type="button" (click)="clear()">Clear the search</button>
          </div>
        }
      }
    </section>
    <app-footer />
  `,
  styleUrl: './skills.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Skills {
  private readonly api = inject(ApiService);
  private readonly router = inject(Router);

  /** Bound from the ?stage= query parameter. */
  readonly stage = input<string>();

  protected readonly query = signal('');
  protected readonly catalog = toSignal(this.api.catalog().pipe(catchError(() => of(null))), { initialValue: undefined });
  protected readonly activeStage = computed(() => {
    const n = Number(this.stage());
    return Number.isInteger(n) && n > 0 ? n : null;
  });

  protected readonly groups = computed(() => {
    const data = this.catalog();
    if (!data) return [];
    const terms = this.query().toLowerCase().split(/\s+/).filter(Boolean);
    const stage = this.activeStage();
    const matches = (s: SkillBrief) => {
      if (stage && s.stage_index !== stage) return false;
      const text = `${s.name} ${s.title} ${s.summary} ${s.description} ${s.tags.join(' ')} ${s.stage}`.toLowerCase();
      return terms.every((t) => text.includes(t));
    };
    return data.stages
      .map((st) => ({ ...st, skills: data.skills.filter((s) => s.stage_index === st.index && matches(s)) }))
      .filter((g) => g.skills.length);
  });

  protected setStage(stage: number | null): void {
    this.router.navigate([], { queryParams: { stage }, queryParamsHandling: 'merge', replaceUrl: true });
  }

  protected clear(): void {
    this.query.set('');
    this.setStage(null);
  }

  protected reload(): void {
    location.reload();
  }
}
