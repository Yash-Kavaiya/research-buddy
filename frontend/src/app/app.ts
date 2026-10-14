import { DOCUMENT } from '@angular/common';
import { ChangeDetectionStrategy, Component, DestroyRef, computed, inject, signal } from '@angular/core';
import { NavigationEnd, Router, RouterLink, RouterLinkActive, RouterOutlet } from '@angular/router';
import { filter } from 'rxjs';

import { SettingsStore, Theme } from './core/settings.store';
import { Icon } from './shared/icon';
import { RatePrompt } from './shared/rate-prompt';

const NEXT_THEME: Record<Theme, Theme> = { system: 'light', light: 'dark', dark: 'system' };
const THEME_ICON: Record<Theme, string> = { system: 'auto', light: 'sun', dark: 'moon' };

interface NavItem {
  path: string;
  label: string;
  icon: string;
  exact?: boolean;
}

const NAV: NavItem[] = [
  { path: '/', label: 'Home', icon: 'home', exact: true },
  { path: '/workspace', label: 'Research', icon: 'search' },
  { path: '/skills', label: 'Library', icon: 'library' },
  { path: '/connectors', label: 'Connectors', icon: 'plug' },
  { path: '/settings', label: 'Settings', icon: 'gear' },
];

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, RouterLink, RouterLinkActive, Icon, RatePrompt],
  template: `
    <a class="skip" href="#main">Skip to content</a>

    <nav class="rail" data-nav aria-label="Main">
      <a class="brand" routerLink="/" aria-label="Research Buddy home" title="Research Buddy">
        <svg width="20" height="20" viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d="M12 2l2.2 7.3L21.5 12l-7.3 2.2L12 21.5l-2.2-7.3L2.5 12l7.3-2.7z" />
        </svg>
      </a>
      <div class="rail-links">
        @for (item of nav; track item.path) {
          <a
            class="rail-link"
            [routerLink]="item.path"
            routerLinkActive="on"
            [routerLinkActiveOptions]="{ exact: !!item.exact }"
            [attr.aria-label]="item.label"
            [attr.data-label]="item.label"
          >
            <app-icon [name]="item.icon" [size]="20" />
          </a>
        }
      </div>
      <div class="rail-foot">
        <a class="rail-link" routerLink="/support" routerLinkActive="on" aria-label="Support" data-label="Support">
          <app-icon name="heart" [size]="19" />
        </a>
        <button class="rail-link" type="button" (click)="cycleTheme()" [attr.aria-label]="themeLabel()" [attr.data-label]="themeShort()">
          <app-icon [name]="themeIcon()" [size]="19" />
        </button>
      </div>
    </nav>

    <header class="topbar" data-nav>
      <button class="icon-btn" type="button" (click)="menuOpen.set(!menuOpen())" [attr.aria-expanded]="menuOpen()" aria-label="Menu">
        <app-icon [name]="menuOpen() ? 'close' : 'menu'" [size]="20" />
      </button>
      <a class="top-brand" routerLink="/">
        <svg width="16" height="16" viewBox="0 0 24 24" aria-hidden="true">
          <path fill="currentColor" d="M12 2l2.2 7.3L21.5 12l-7.3 2.2L12 21.5l-2.2-7.3L2.5 12l7.3-2.7z" />
        </svg>
        Research Buddy
      </a>
      <button class="icon-btn" type="button" (click)="cycleTheme()" [attr.aria-label]="themeLabel()">
        <app-icon [name]="themeIcon()" [size]="19" />
      </button>
      @if (menuOpen()) {
        <div class="drawer">
          @for (item of nav; track item.path) {
            <a [routerLink]="item.path" routerLinkActive="on" [routerLinkActiveOptions]="{ exact: !!item.exact }">
              <app-icon [name]="item.icon" [size]="18" />
              {{ item.label }}
            </a>
          }
          <a routerLink="/support" routerLinkActive="on"><app-icon name="heart" [size]="18" /> Support</a>
        </div>
      }
    </header>
    @if (menuOpen()) {
      <button class="scrim" type="button" aria-label="Close menu" (click)="menuOpen.set(false)"></button>
    }

    <main id="main" tabindex="-1">
      <router-outlet />
    </main>
    <app-rate-prompt />
  `,
  styles: `
    :host {
      display: grid;
      grid-template-columns: var(--rail-width) minmax(0, 1fr);
      min-height: 100dvh;
      --chrome-top: 0px;
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

    .rail {
      position: sticky;
      top: 0;
      z-index: 50;
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 18px;
      height: 100dvh;
      padding: 14px 0 16px;
      border-right: 1px solid var(--border);
      background: var(--bg-alt);
    }

    .brand {
      display: grid;
      place-items: center;
      width: 38px;
      height: 38px;
      border-radius: 12px;
      background: var(--accent);
      color: var(--on-accent);
      box-shadow: 0 6px 16px -6px var(--accent);
      transition: transform 0.2s var(--ease);

      &:hover {
        transform: rotate(-8deg) scale(1.04);
      }
    }

    .rail-links,
    .rail-foot {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 6px;
      width: 100%;
    }

    .rail-foot {
      margin-top: auto;
    }

    .rail-link {
      position: relative;
      display: grid;
      place-items: center;
      width: 42px;
      height: 42px;
      padding: 0;
      border: 0;
      border-radius: 12px;
      background: transparent;
      color: var(--text-3);
      transition: background 0.15s var(--ease), color 0.15s var(--ease);

      &:hover {
        background: var(--bg-inset);
        color: var(--text);
        text-decoration: none;
      }

      &.on {
        background: var(--accent-tint);
        color: var(--accent);

        &::before {
          content: '';
          position: absolute;
          left: -11px;
          top: 9px;
          bottom: 9px;
          width: 3px;
          border-radius: 0 3px 3px 0;
          background: var(--accent);
        }
      }

      // Tooltip
      &::after {
        content: attr(data-label);
        position: absolute;
        left: calc(100% + 10px);
        top: 50%;
        padding: 5px 9px;
        border-radius: 7px;
        background: var(--text);
        color: var(--bg);
        font-size: 12px;
        font-weight: 500;
        white-space: nowrap;
        opacity: 0;
        pointer-events: none;
        transform: translate(-4px, -50%);
        transition: opacity 0.15s var(--ease), transform 0.15s var(--ease);
      }

      &:hover::after,
      &:focus-visible::after {
        opacity: 1;
        transform: translate(0, -50%);
      }
    }

    .topbar,
    .scrim {
      display: none;
    }

    main {
      display: flex;
      flex-direction: column;
      min-width: 0;
      min-height: 0;
      outline: none;
    }

    @media (max-width: 767px) {
      :host {
        grid-template-columns: minmax(0, 1fr);
        --chrome-top: var(--nav-height);
      }

      .rail {
        display: none;
      }

      .topbar {
        position: sticky;
        top: 0;
        z-index: 60;
        display: flex;
        align-items: center;
        justify-content: space-between;
        height: var(--nav-height);
        padding: 0 10px;
        border-bottom: 1px solid var(--border);
        background: var(--nav-bg);
        backdrop-filter: saturate(160%) blur(16px);
        -webkit-backdrop-filter: saturate(160%) blur(16px);
      }

      .top-brand {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: var(--text);
        font-family: var(--font-display);
        font-size: 16px;
        font-weight: 700;

        svg {
          color: var(--accent);
        }

        &:hover {
          text-decoration: none;
        }
      }

      .drawer {
        position: absolute;
        top: calc(100% + 1px);
        left: 0;
        right: 0;
        display: grid;
        gap: 2px;
        padding: 10px;
        border-bottom: 1px solid var(--border);
        background: var(--bg-elevated);
        box-shadow: var(--shadow-raised);

        a {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 12px 14px;
          border-radius: var(--radius-m);
          color: var(--text);
          font-weight: 500;

          &:hover {
            background: var(--bg-inset);
            text-decoration: none;
          }

          &.on {
            background: var(--accent-tint);
            color: var(--accent);
          }
        }
      }

      .scrim {
        display: block;
        position: fixed;
        inset: var(--nav-height) 0 0;
        z-index: 55;
        border: 0;
        background: rgba(13, 15, 19, 0.3);
      }
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class App {
  private readonly settings = inject(SettingsStore);
  private readonly document = inject(DOCUMENT);

  protected readonly nav = NAV;
  protected readonly menuOpen = signal(false);

  constructor() {
    const open = (event: Event) => this.openInNewTab(event as MouseEvent);
    this.document.addEventListener('click', open, true);
    inject(DestroyRef).onDestroy(() => this.document.removeEventListener('click', open, true));
    inject(Router)
      .events.pipe(filter((e) => e instanceof NavigationEnd))
      .subscribe(() => this.menuOpen.set(false));
  }

  /** Every link outside the main navigation opens in a new tab. The navigation stays in this tab. */
  private openInNewTab(event: MouseEvent): void {
    if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) {
      return;
    }
    const anchor = (event.target as HTMLElement | null)?.closest('a');
    if (!anchor || anchor.classList.contains('skip') || anchor.closest('[data-nav]')) return;
    const href = anchor.getAttribute('href') ?? '';
    if (!href || href.startsWith('#') || href.startsWith('mailto:') || href.startsWith('javascript:')) return;
    event.preventDefault();
    event.stopPropagation();
    window.open(anchor.href, '_blank', 'noopener,noreferrer');
  }

  protected readonly themeIcon = computed(() => THEME_ICON[this.settings.theme()]);
  protected readonly themeShort = computed(() => {
    const theme = this.settings.theme();
    return `Appearance: ${theme === 'system' ? 'auto' : theme}`;
  });
  protected readonly themeLabel = computed(() => `${this.themeShort()}. Click to change.`);

  protected cycleTheme(): void {
    this.settings.setTheme(NEXT_THEME[this.settings.theme()]);
  }
}
