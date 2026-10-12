import { ChangeDetectionStrategy, Component, computed, inject, input } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

import { renderMarkdown } from '../core/markdown';

@Component({
  selector: 'app-markdown',
  template: `<div class="md" [innerHTML]="html()"></div>`,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Markdown {
  private readonly sanitizer = inject(DomSanitizer);

  readonly source = input.required<string>();
  // renderMarkdown sanitizes with DOMPurify; Angular's own sanitizer would strip KaTeX's inline styles.
  protected readonly html = computed(() => this.sanitizer.bypassSecurityTrustHtml(renderMarkdown(this.source())));
}
