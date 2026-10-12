import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { ActivatedRoute, RouterLink } from '@angular/router';
import { catchError, of, switchMap } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { Footer } from '../../shared/footer';
import { Markdown } from '../../shared/markdown';

@Component({
  selector: 'app-skill-detail',
  imports: [RouterLink, Footer, Markdown],
  template: `
    <div class="page-narrow wrap">
      @if (skill(); as s) {
        <a class="back" routerLink="/skills">Skills</a>
        <span class="eyebrow">{{ s.stageName }}</span>
        <h1>{{ s.name }}</h1>
        <p class="lede">{{ s.description }}</p>
        <div class="actions">
          <a class="btn" [routerLink]="'/workspace'" [queryParams]="{ skill: s.name }">Use in workspace</a>
          @if (s.hasScripts) {
            <span class="pill">{{ s.scripts.join(', ') }}</span>
          }
        </div>
        <app-markdown [source]="s.body" />
      } @else if (skill() === null) {
        <h1>Skill not found</h1>
        <p><a routerLink="/skills">Back to the library</a></p>
      }
      <app-footer />
    </div>
  `,
  styles: `
    .wrap {
      h1 {
        font-size: 36px;
        margin: 4px 0 12px;
      }
    }
    .back {
      display: inline-block;
      margin-bottom: 18px;
      color: var(--text-2);
      font-size: 14px;
    }
    .lede {
      font-size: 18px;
    }
    .actions {
      display: flex;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
      margin: 22px 0 32px;
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SkillDetailPage {
  private readonly api = inject(ApiService);
  private readonly route = inject(ActivatedRoute);
  protected readonly skill = toSignal(
    this.route.paramMap.pipe(
      switchMap((params) => this.api.skill(params.get('name') ?? '').pipe(catchError(() => of(null)))),
    ),
  );
}
