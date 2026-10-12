import { ChangeDetectionStrategy, Component } from '@angular/core';
import { RouterLink } from '@angular/router';

@Component({
  selector: 'app-footer',
  imports: [RouterLink],
  template: `
    <footer>
      <p>
        Research Buddy uses the
        <a href="https://github.com/Yash-Kavaiya/research-scholar-agent-skills" rel="noopener noreferrer" target="_blank"
          >research-scholar agent skills</a
        >. You bring your own model key; nothing is stored on the server.
      </p>
      <p>
        <a routerLink="/settings">Settings</a>
        ·
        <a routerLink="/connectors">Connectors</a>
        ·
        <a routerLink="/support">Support this project</a>
        ·
        <a routerLink="/skills">Skill library</a>
      </p>
      <p class="fineprint">
        Research Buddy can make mistakes. Verify citations, statistics, and venue rules before you rely on them.
        Decisions stay with you.
      </p>
    </footer>
  `,
  styles: `
    footer {
      margin-top: 64px;
      padding: 28px 0 8px;
      border-top: 1px solid var(--border);
      color: var(--text-3);
      font-size: 13px;
      letter-spacing: -0.01em;
    }

    p + p {
      margin-top: 8px;
    }

    a {
      color: var(--text-2);
    }

    .fineprint {
      margin-top: 10px;
      font-size: 11px;
      line-height: 1.4;
      color: var(--text-3);
    }
  `,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Footer {}
