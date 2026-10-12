import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-footer',
  imports: [RouterLink],
  template: `
    <footer>
      <div class="container inner">
        <p>
          Research Buddy helps you plan, analyse, draft, and check. The decisions, the data, and what you submit
          remain yours. Disclose AI assistance as your venue or institution requires.
        </p>
        <nav aria-label="Footer">
          <a routerLink="/skills">Skills</a>
          <a routerLink="/workspace">Workspace</a>
          <a routerLink="/settings">Settings</a>
          <a href="https://github.com/Yash-Kavaiya/research-scholar-agent-skills" target="_blank" rel="noopener">Skills on GitHub</a>
          <a href="https://github.com/Yash-Kavaiya/research-buddy" target="_blank" rel="noopener">Source</a>
        </nav>
      </div>
    </footer>
  `,
  styles: `
    footer {
      margin-top: auto;
      padding: 28px 0 36px;
      background: var(--bg-alt);
      color: var(--text-2);
      font-size: 12px;
      line-height: 1.5;
      letter-spacing: -0.005em;
    }

    .inner {
      display: grid;
      gap: 14px;
    }

    p {
      max-width: 720px;
    }

    nav {
      display: flex;
      flex-wrap: wrap;
      gap: 6px 22px;
      padding-top: 14px;
      border-top: 1px solid var(--border);

      a {
        color: var(--text-2);
      }
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Footer {}
