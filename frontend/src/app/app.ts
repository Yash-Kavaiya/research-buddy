import { ChangeDetectionStrategy, Component, computed, inject } from '@angular/core';
import { RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';

import { SettingsStore, Theme } from './core/settings.store';
import { Icon } from './shared/icon';

const NEXT_THEME: Record<Theme, Theme> = { system: 'light', light: 'dark', dark: 'system' };
const THEME_ICON: Record<Theme, string> = { system: 'auto', light: 'sun', dark: 'moon' };

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive, Icon],
  template: `
    <a class="skip" href="#main">Skip to content</a>
    <header class="nav">
      <nav class="nav-inner" aria-label="Main">
        <a class="brand" routerLink="/" aria-label="Research Buddy home">
          <img src="favicon.svg" width="22" height="22" alt="" />
          <span>Research Buddy</span>
        </a>
        <div class="links">
          <a routerLink="/skills" routerLinkActive="on">Skills</a>
          <a routerLink="/workspace" routerLinkActive="on">Workspace</a>
          <a routerLink="/settings" routerLinkActive="on">Settings</a>
        </div>
        <button class="icon-btn theme" type="button" (click)="cycleTheme()" [attr.aria-label]="themeLabel()" [title]="themeLabel()">
          <app-icon [name]="themeIcon()" [size]="17" />
        </button>
      </nav>
    </header>
    <main id="main" tabindex="-1">
      <router-outlet />
    </main>
  `,
  styles: `
    :host {
      display: flex;
      flex-direction: column;
      min-height: 100dvh;
    }

    .skip {
      position: absolute;
      left: 12px;
      top: -60px;
      z-index: 100;
      padding: 8px 14px;
      border-radius: var(--radius-s);
      background: var(--accent);
      color: var(--on-accent);

      &:focus {
        top: 8px;
      }
    }

    .nav {
      position: sticky;
      top: 0;
      z-index: 50;
      height: var(--nav-height);
      background: var(--nav-bg);
      backdrop-filter: saturate(180%) blur(20px);
      -webkit-backdrop-filter: saturate(180%) blur(20px);
      border-bottom: 1px solid var(--border);
    }

    .nav-inner {
      display: flex;
      align-items: center;
      gap: 8px;
      height: 100%;
      max-width: calc(var(--page-width) + 2 * var(--gutter));
      margin-inline: auto;
      padding-inline: var(--gutter);
    }

    .brand {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      margin-right: auto;
      color: var(--text);
      font-size: 15px;
      font-weight: 600;
      letter-spacing: -0.015em;

      &:hover {
        text-decoration: none;
      }

      img {
        border-radius: 6px;
      }
    }

    .links {
      display: flex;
      gap: clamp(2px, 2vw, 20px);

      a {
        padding: 6px 8px;
        border-radius: var(--radius-s);
        color: var(--text);
        font-size: 13px;
        letter-spacing: -0.008em;
        opacity: 0.8;
        transition: opacity 0.2s var(--ease);

        &:hover,
        &.on {
          opacity: 1;
          text-decoration: none;
        }

        &.on {
          font-weight: 600;
        }
      }
    }

    .theme {
      width: 32px;
      height: 32px;
      margin-right: -6px;
    }

    main {
      flex: 1;
      display: flex;
      flex-direction: column;
      min-height: 0;
      outline: none;
    }

    @media (max-width: 480px) {
      .brand span {
        display: none;
      }
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class App {
  private readonly settings = inject(SettingsStore);

  protected readonly themeIcon = computed(() => THEME_ICON[this.settings.theme()]);
  protected readonly themeLabel = computed(() => {
    const theme = this.settings.theme();
    return `Appearance: ${theme === 'system' ? 'automatic' : theme}. Click to change.`;
  });

  protected cycleTheme(): void {
    this.settings.setTheme(NEXT_THEME[this.settings.theme()]);
  }
}
