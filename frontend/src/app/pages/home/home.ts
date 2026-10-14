import { ChangeDetectionStrategy, Component, inject, signal } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { Router, RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { SkillSummary } from '../../core/models';
import { Footer } from '../../shared/footer';
import { Icon } from '../../shared/icon';

const STARTERS = [
  'Find recent papers on retrieval-augmented generation and summarise the main approaches',
  'How many participants per group for a two-sample t-test with d = 0.5 and power 0.8?',
  'Turn my interest in federated learning for medical imaging into a FINER research question',
  'Check whether the references in my BibTeX file are real',
];

@Component({
  selector: 'app-home',
  imports: [RouterLink, Footer, Icon],
  templateUrl: './home.html',
  styleUrl: './home.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Home {
  private readonly api = inject(ApiService);
  private readonly router = inject(Router);

  protected readonly starters = STARTERS;
  protected readonly question = signal('');
  protected readonly catalog = toSignal(this.api.catalog().pipe(catchError(() => of(null))), {
    initialValue: null,
  });

  protected ask(text = this.question()): void {
    const q = text.trim();
    if (q) void this.router.navigate(['/workspace'], { queryParams: { q } });
  }

  protected onKey(event: KeyboardEvent): void {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      this.ask();
    }
  }

  protected countFor(skills: SkillSummary[], stage: string): number {
    return skills.filter((s) => s.stage === stage).length;
  }

  protected pad(n: number): string {
    return String(n).padStart(2, '0');
  }
}
