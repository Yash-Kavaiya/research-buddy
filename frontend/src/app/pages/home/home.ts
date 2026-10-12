import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { toSignal } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { ApiService } from '../../core/api.service';
import { Footer } from '../../shared/footer';
import { Icon } from '../../shared/icon';

interface Example {
  prompt: string;
  skill: string;
}

@Component({
  selector: 'app-home',
  imports: [RouterLink, Icon, Footer],
  templateUrl: './home.html',
  styleUrl: './home.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Home {
  private readonly api = inject(ApiService);
  private readonly catalog = toSignal(this.api.catalog().pipe(catchError(() => of(null))), { initialValue: undefined });

  protected readonly stages = computed(() => {
    const catalog = this.catalog();
    if (!catalog) return [];
    return catalog.stages.map((stage) => ({
      ...stage,
      skills: catalog.skills.filter((s) => s.stage_index === stage.index).map((s) => s.title),
    }));
  });
  protected readonly failed = computed(() => this.catalog() === null);
  protected readonly placeholders = Array.from({ length: 12 });

  protected readonly examples: Example[] = [
    { prompt: 'Find research gaps in federated learning for medical imaging', skill: 'research-gap-finder' },
    { prompt: 'How many participants do I need for a two-group comparison with d = 0.5?', skill: 'sample-size-power-calculator' },
    { prompt: 'Check whether the references in my .bib file are real', skill: 'citation-verifier' },
    { prompt: 'Review my paper like Reviewer 2 before I submit to ACL', skill: 'self-peer-reviewer' },
    { prompt: 'Turn results.csv into a LaTeX table with the best results in bold', skill: 'latex-table-generator' },
    { prompt: 'I have results and a deadline in three weeks. What do I do next?', skill: 'research-scholar-orchestrator' },
  ];

  protected readonly providers = ['Google Gemini', 'OpenAI', 'Anthropic', 'Groq', 'OpenRouter', 'NVIDIA NIM'];
}
