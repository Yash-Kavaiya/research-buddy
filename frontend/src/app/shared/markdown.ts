import { ChangeDetectionStrategy, Component, computed, inject, input, output } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

import { renderMarkdown } from '../core/markdown';

@Component({
  selector: 'app-markdown',
  template: `<div class="md" [innerHTML]="html()" (click)="onClick($event)"></div>`,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Markdown {
  readonly source = input('');
  /** Render [n] markers as citation chips. */
  readonly cites = input(false);
  /** Emits the citation number when a chip is clicked. */
  readonly cite = output<number>();
  private readonly sanitizer = inject(DomSanitizer);
  protected readonly html = computed(() =>
    this.sanitizer.bypassSecurityTrustHtml(renderMarkdown(this.source(), this.cites())),
  );

  protected onClick(event: MouseEvent): void {
    const chip = (event.target as HTMLElement | null)?.closest<HTMLElement>('.cite');
    if (chip?.dataset['cite']) this.cite.emit(Number(chip.dataset['cite']));
  }
}
