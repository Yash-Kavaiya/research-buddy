import { ChangeDetectionStrategy, Component, computed, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, map, of } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { SkillSummary } from '../../core/models';
import { Footer } from '../../shared/footer';
import { Icon } from '../../shared/icon';

@Component({
  selector: 'app-skills',
  imports: [RouterLink, Footer, Icon],
  template: `
    <div class="page">
      <header class="head">
        <span class="eyebrow">Library</span>
        <h1>Skills</h1>
        <p>Each skill is a set of instructions the assistant loads before it works. Scripts run when the answer has to be retrieved or computed.</p>
      </header>

      @if (catalog(); as cat) {
        <div class="toolbar">
          <label class="search">
            <app-icon name="search" [size]="16" />
            <input type="search" placeholder="Search skills" [value]="query()" (input)="query.set($any($event.target).value)" />
          </label>
          <div class="filters" role="tablist" aria-label="Stage">
            <button type="button" [class.on]="!stage()" (click)="setStage(null)">All</button>
            @for (s of cat.stages; track s.id) {
              <button type="button" [class.on]="stage() === s.id" (click)="setStage(s.id)">{{ s.name }}</button>
            }
          </div>
        </div>

        <div class="list">
          @for (skill of filtered(); track skill.name) {
            <a class="item card" [routerLink]="['/skills', skill.name]">
              <i class="dot" [style.background]="'var(--stage-' + skill.stageNumber + ')'"></i>
              <div>
                <strong>{{ skill.name }}</strong>
                <span class="desc">{{ skill.description }}</span>
                <span class="meta">{{ skill.stageName }}@if (skill.hasScripts) { · script}</span>
              </div>
              <app-icon name="chevron" [size]="16" />
            </a>
          } @empty {
            <p>No skills match that search.</p>
          }
        </div>
      } @else if (failed()) {
        <p class="banner banner-warn">Could not load the skill library. Is the API running?</p>
      }

      <app-footer />
    </div>
  `,
  styleUrl: './skills.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Skills {
  private readonly api = inject(ApiService);
  private readonly route = inject(ActivatedRoute);

  protected readonly query = signal('');
  protected readonly stage = signal<string | null>(this.route.snapshot.queryParamMap.get('stage'));
  protected readonly failed = signal(false);
  protected readonly catalog = toSignal(
    this.api.catalog().pipe(
      catchError(() => {
        this.failed.set(true);
        return of(null);
      }),
    ),
    { initialValue: null },
  );

  protected readonly filtered = computed(() => {
    const cat = this.catalog();
    if (!cat) return [];
    const q = this.query().trim().toLowerCase();
    const stage = this.stage();
    return cat.skills.filter((s) => matches(s, q, stage));
  });

  protected setStage(id: string | null): void {
    this.stage.set(id);
  }
}

function matches(skill: SkillSummary, q: string, stage: string | null): boolean {
  if (stage && skill.stage !== stage) return false;
  if (!q) return true;
  return (
    skill.name.includes(q) ||
    skill.description.toLowerCase().includes(q) ||
    skill.tags.some((t) => t.toLowerCase().includes(q))
  );
}
