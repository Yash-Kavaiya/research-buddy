import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { SkillSummary } from '../../core/models';
import { Footer } from '../../shared/footer';

@Component({
  selector: 'app-home',
  imports: [RouterLink, Footer],
  templateUrl: './home.html',
  styleUrl: './home.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Home {
  private readonly api = inject(ApiService);
  protected readonly catalog = toSignal(this.api.catalog().pipe(catchError(() => of(null))), {
    initialValue: null,
  });

  protected countFor(skills: SkillSummary[], stage: string): number {
    return skills.filter((s) => s.stage === stage).length;
  }
}
