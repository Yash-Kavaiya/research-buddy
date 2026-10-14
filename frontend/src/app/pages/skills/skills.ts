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
        <h1>Research skills</h1>
        <p>Each skill is a method the assistant loads before it works. Skills with scripts retrieve or compute part of the answer instead of guessing it.</p>
      </header>

      @if (catalog(); as cat) {
        <div class="toolbar">
          <label class="search">
            <app-icon name="search" [size]="17" />
            <input type="search" placeholder="Search {{ cat.skills.length }} skills by name, topic or tag" [value]="query()" (input)="query.set($any($event.target).value)" />
            <span class="mono found">{{ filtered().length }}</span>
          </label>
          <div class="filters" role="tablist" aria-label="Stage">
            <button type="button" [class.on]="!stage()" (click)="setStage(null)">All stages</button>
            @for (s of cat.stages; track s.id) {
              <button type="button" [class.on]="stage() === s.id" (click)="setStage(s.id)">
                <i class="dot" [style.background]="'var(--stage-' + s.number + ')'"></i>{{ s.name }}
              </button>
            }
          </div>
        </div>

        <div class="list">
          @for (skill of filtered(); track skill.name) {
            <a class="item" [routerLink]="['/skills', skill.name]">
              <span class="top">
                <span class="stage-tag mono" [style.color]="'var(--stage-' + skill.stageNumber + ')'">
                  {{ skill.stageNumber < 10 ? '0' + skill.stageNumber : skill.stageNumber }}
                </span>
                <span class="stage-name">{{ skill.stageName }}</span>
                @if (skill.hasScripts) {
                  <span class="script mono"><app-icon name="terminal" [size]="12" /> script</span>
                }
              </span>
              <strong class="mono">{{ skill.name }}</strong>
              <span class="desc">{{ skill.description }}</span>
            </a>
          } @empty {
            <p class="none">No skills match that search.</p>
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
