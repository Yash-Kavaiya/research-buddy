import { ChangeDetectionStrategy, Component, computed, inject, signal } from '@angular/core';
import { Subscription } from 'rxjs';
import { toSignal } from '@angular/core/rxjs-interop';
import { RouterLink } from '@angular/router';
import { catchError, of } from 'rxjs';

import { ApiService, errorMessage } from '../../core/api.service';
import { ChatStore } from '../../core/chat.store';
import { KeyCheck } from '../../core/models';
import { SettingsStore, Theme } from '../../core/settings.store';
import { Footer } from '../../shared/footer';
import { Icon } from '../../shared/icon';

@Component({
  selector: 'app-settings',
  imports: [RouterLink, Icon, Footer],
  templateUrl: './settings.html',
  styleUrl: './settings.scss',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class Settings {
  private readonly api = inject(ApiService);
  protected readonly settings = inject(SettingsStore);
  protected readonly chats = inject(ChatStore);

  protected readonly providers = toSignal(this.api.providers().pipe(catchError(() => of(null))), { initialValue: undefined });
  protected readonly provider = computed(() => this.providers()?.find((p) => p.id === this.settings.provider()) ?? null);

  protected readonly showKey = signal(false);
  protected readonly checking = signal(false);
  protected readonly check = signal<KeyCheck | null>(null);
  protected readonly cleared = signal('');
  protected readonly models = signal<string[]>([]);
  protected readonly loadingModels = signal(false);
  protected readonly modelsError = signal('');
  private modelsRequest?: Subscription;

  protected readonly themes: { id: Theme; label: string; icon: string }[] = [
    { id: 'system', label: 'Automatic', icon: 'auto' },
    { id: 'light', label: 'Light', icon: 'sun' },
    { id: 'dark', label: 'Dark', icon: 'moon' },
  ];

  protected chooseProvider(id: string): void {
    this.settings.setProvider(id);
    this.check.set(null);
    this.loadModels();
  }

  /** Ask the provider which models this key can use. */
  protected loadModels(): void {
    this.modelsRequest?.unsubscribe();
    this.models.set([]);
    this.modelsError.set('');
    const key = this.settings.apiKey();
    if (!key) {
      this.loadingModels.set(false);
      return;
    }
    this.loadingModels.set(true);
    this.modelsRequest = this.api.models(this.settings.provider(), key).subscribe({
      next: (models) => {
        this.models.set(models);
        this.loadingModels.set(false);
      },
      error: (error) => {
        this.modelsError.set(errorMessage(error));
        this.loadingModels.set(false);
      },
    });
  }

  protected setModel(model: string): void {
    this.settings.setModel(this.settings.provider(), model);
    this.check.set(null);
  }

  protected setKey(key: string): void {
    this.settings.setKey(this.settings.provider(), key);
    this.check.set(null);
  }

  protected test(): void {
    if (!this.settings.ready() || this.checking()) return;
    this.checking.set(true);
    this.check.set(null);
    this.api
      .validateKey(this.settings.provider(), this.settings.model(), this.settings.apiKey())
      .subscribe((result) => {
        this.check.set(result);
        this.checking.set(false);
      });
  }

  protected clearChats(): void {
    this.chats.clearAll();
    this.cleared.set('Conversations removed from this browser.');
  }

  protected clearKeys(): void {
    this.settings.clearSecrets();
    this.check.set(null);
    this.cleared.set('API keys removed from this browser.');
  }

  constructor() {
    this.loadModels();
  }
}
