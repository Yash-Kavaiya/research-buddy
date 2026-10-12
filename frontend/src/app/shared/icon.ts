import { ChangeDetectionStrategy, Component, input } from '@angular/core';

const PATHS: Record<string, string> = {
  auto: 'M12 3a9 9 0 1 0 9 9h-9V3z M12 3v9h9A9 9 0 0 0 12 3z',
  sun: 'M12 4V2M12 22v-2M4.93 4.93 3.51 3.51M20.49 20.49l-1.42-1.42M4 12H2M22 12h-2M4.93 19.07 3.51 20.49M20.49 3.51l-1.42 1.42M12 8a4 4 0 1 0 0 8 4 4 0 0 0 0-8z',
  moon: 'M21 14.3A8.5 8.5 0 0 1 9.7 3 7 7 0 1 0 21 14.3z',
  send: 'M3.4 20.6 21 12 3.4 3.4 3 10l11 2-11 2z',
  stop: 'M7 7h10v10H7z',
  attach: 'M21.4 11.6 12.2 20.8a6 6 0 0 1-8.5-8.5l9.2-9.2a4 4 0 0 1 5.7 5.7l-9.2 9.1a2 2 0 1 1-2.8-2.8l8.5-8.5',
  copy: 'M8 8h10v12H8z M6 16H4V4h12v2',
  plus: 'M12 5v14M5 12h14',
  trash: 'M4 7h16M9 7V5h6v2M8 7l1 12h6l1-12',
  chevron: 'M9 6l6 6-6 6',
  spark: 'M12 3l1.5 6L20 10.5 13.5 12 12 18l-1.5-6L4 10.5 10.5 9z',
  check: 'M5 13l4 4L19 7',
  close: 'M6 6l12 12M18 6 6 18',
  menu: 'M4 7h16M4 12h16M4 17h16',
  key: 'M8 14a4 4 0 1 1 3.5-2H22v3h-2v2h-3v-2h-2v-3h-3.5A4 4 0 0 1 8 14z',
  search: 'M11 5a6 6 0 1 0 0 12 6 6 0 0 0 0-12zM20 20l-4-4',
  up: 'M14 10V6a2 2 0 0 0-2-2l-1 5H6a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h8.2a2 2 0 0 0 1.9-1.4l1.5-5.1A2 2 0 0 0 15.7 10H14z',
  down: 'M10 14v4a2 2 0 0 0 2 2l1-5h5a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2H9.8A2 2 0 0 0 7.9 6.4L6.4 11.5A2 2 0 0 0 8.3 14H10z',
  share: 'M4 12v7a1 1 0 0 0 1 1h14a1 1 0 0 0 1-1v-7M16 6l-4-4-4 4M12 2v13',
  branch: 'M6 3a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM6 16a2.5 2.5 0 1 0 0 5 2.5 2.5 0 0 0 0-5zM18 8a2.5 2.5 0 1 0 0-5 2.5 2.5 0 0 0 0 5zM6 8v8M18 8c0 3-4 4-7 4H6',
  folder: 'M3 7.5A1.5 1.5 0 0 1 4.5 6H9l2 2h8.5A1.5 1.5 0 0 1 21 9.5v8A1.5 1.5 0 0 1 19.5 19h-15A1.5 1.5 0 0 1 3 17.5z',
  code: 'M8 8 4 12l4 4M16 8l4 4-4 4M13 6l-2 12',
};

@Component({
  selector: 'app-icon',
  template: `
    <svg
      [attr.width]="size()"
      [attr.height]="size()"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      stroke-width="1.8"
      stroke-linecap="round"
      stroke-linejoin="round"
      aria-hidden="true"
    >
      <path [attr.d]="PATHS[name()] || ''" />
    </svg>
  `,
  styles: `
    :host {
      display: inline-flex;
      line-height: 0;
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Icon {
  readonly name = input.required<string>();
  readonly size = input(18);
  protected readonly PATHS = PATHS;
}
