import { ChangeDetectionStrategy, Component, computed, inject, input } from '@angular/core';
import { DomSanitizer } from '@angular/platform-browser';

import { renderMarkdown } from '../core/markdown';

@Component({
  selector: 'app-markdown',
  template: `<div class="md" [innerHTML]="html()"></div>`,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Markdown {
  readonly source = input('');
  private readonly sanitizer = inject(DomSanitizer);
  protected readonly html = computed(() => this.sanitizer.bypassSecurityTrustHtml(renderMarkdown(this.source())));
}
