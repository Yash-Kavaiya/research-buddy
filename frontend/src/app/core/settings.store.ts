import { DOCUMENT } from '@angular/common';
import { Injectable, computed, effect, inject, signal } from '@angular/core';

import { readJson, remove, storage, writeJson } from './storage';

export type Theme = 'system' | 'light' | 'dark';

interface Preferences {
  provider: string;
  models: Record<string, string>;
  theme: Theme;
  rememberKeys: boolean;
}

interface Secrets {
  llm: Record<string, string>;
  s2: string;
  ncbi: string;
}

const PREFS_KEY = 'rb.preferences';
const SECRETS_KEY = 'rb.secrets';
const DEFAULT_PREFS: Preferences = { provider: 'google', models: {}, theme: 'system', rememberKeys: true };
const NO_SECRETS: Secrets = { llm: {}, s2: '', ncbi: '' };

/**
 * The user's provider, model, and API keys. Keys never leave the browser except as
 * request headers to this site's own API. They are kept in localStorage, or in
 * sessionStorage when the user chooses not to remember them.
 */
@Injectable({ providedIn: 'root' })
export class SettingsStore {
  private readonly document = inject(DOCUMENT);
  private readonly prefs = signal<Preferences>({ ...DEFAULT_PREFS, ...readJson(storage('local'), PREFS_KEY, {}) });
  private readonly secrets = signal<Secrets>({
    ...NO_SECRETS,
    ...readJson(storage(this.prefs().rememberKeys ? 'local' : 'session'), SECRETS_KEY, {}),
  });

  readonly provider = computed(() => this.prefs().provider);
  readonly theme = computed(() => this.prefs().theme);
  readonly rememberKeys = computed(() => this.prefs().rememberKeys);
  readonly model = computed(() => this.prefs().models[this.prefs().provider] ?? '');
  readonly apiKey = computed(() => this.secrets().llm[this.prefs().provider] ?? '');
  readonly s2Key = computed(() => this.secrets().s2);
  readonly ncbiKey = computed(() => this.secrets().ncbi);
  readonly ready = computed(() => !!this.apiKey() && !!this.model());

  constructor() {
    effect(() => writeJson(storage('local'), PREFS_KEY, this.prefs()));
    effect(() => {
      const remember = this.prefs().rememberKeys;
      writeJson(storage(remember ? 'local' : 'session'), SECRETS_KEY, this.secrets());
      remove(storage(remember ? 'session' : 'local'), SECRETS_KEY);
    });
    effect(() => {
      const theme = this.prefs().theme;
      const root = this.document.documentElement;
      if (theme === 'system') root.removeAttribute('data-theme');
      else root.setAttribute('data-theme', theme);
    });
  }

  modelFor(provider: string): string {
    return this.prefs().models[provider] ?? '';
  }

  keyFor(provider: string): string {
    return this.secrets().llm[provider] ?? '';
  }

  setProvider(provider: string): void {
    this.prefs.update((p) => ({ ...p, provider }));
  }

  setModel(provider: string, model: string): void {
    this.prefs.update((p) => ({ ...p, models: { ...p.models, [provider]: model.trim() } }));
  }

  setKey(provider: string, key: string): void {
    this.secrets.update((s) => ({ ...s, llm: { ...s.llm, [provider]: key.trim() } }));
  }

  setScholarlyKeys(s2: string, ncbi: string): void {
    this.secrets.update((s) => ({ ...s, s2: s2.trim(), ncbi: ncbi.trim() }));
  }

  setTheme(theme: Theme): void {
    this.prefs.update((p) => ({ ...p, theme }));
  }

  setRememberKeys(rememberKeys: boolean): void {
    this.prefs.update((p) => ({ ...p, rememberKeys }));
  }

  clearSecrets(): void {
    this.secrets.set({ ...NO_SECRETS });
  }

  credentialHeaders(
    provider = this.provider(),
    model = this.model(),
    key = this.apiKey(),
  ): Record<string, string> {
    const headers: Record<string, string> = {
      'X-LLM-Provider': provider,
      'X-LLM-Model': model,
      'X-LLM-Key': key,
    };
    if (this.s2Key()) headers['X-S2-Key'] = this.s2Key();
    if (this.ncbiKey()) headers['X-NCBI-Key'] = this.ncbiKey();
    return headers;
  }
}
