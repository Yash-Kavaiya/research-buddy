import { Injectable, computed, effect, signal } from '@angular/core';

import { Review, Thumb } from './models';
import { readJson, storage, writeJson } from './storage';

const KEY = 'rb.usage';
const FREE_CHATS = 5;

interface UsageState {
  turns: number;
  showAt: number;
  rated: boolean;
  reviews: Review[];
}

const EMPTY: UsageState = { turns: 0, showAt: FREE_CHATS, rated: false, reviews: [] };

/** Counts finished chats on this device and keeps ratings and written reviews. */
@Injectable({ providedIn: 'root' })
export class UsageStore {
  private readonly state = signal<UsageState>(load());
  readonly promptOpen = signal(false);

  readonly turns = computed(() => this.state().turns);
  readonly rated = computed(() => this.state().rated);
  readonly reviews = computed(() => this.state().reviews);

  constructor() {
    effect(() => writeJson(storage('local'), KEY, this.state()));
    const next = this.state();
    if (!next.rated && next.turns >= next.showAt) this.promptOpen.set(true);
  }

  /** Call when an assistant answer finished with real text. */
  completeTurn(): void {
    this.state.update((s) => ({ ...s, turns: s.turns + 1 }));
    const next = this.state();
    if (!next.rated && next.turns >= next.showAt) this.promptOpen.set(true);
  }

  later(): void {
    this.state.update((s) => ({ ...s, showAt: s.turns + FREE_CHATS }));
    this.promptOpen.set(false);
  }

  submit(kind: Thumb | 'review', message: string, source: Review['source']): Review {
    const review: Review = {
      id: uid(),
      kind,
      message: message.trim().slice(0, 4000),
      source,
      at: Date.now(),
    };
    this.state.update((s) => ({
      ...s,
      rated: source === 'popup' || source === 'support' ? true : s.rated,
      reviews: [review, ...s.reviews].slice(0, 50),
    }));
    if (source === 'popup') this.promptOpen.set(false);
    return review;
  }
}

function load(): UsageState {
  const raw = readJson<Partial<UsageState>>(storage('local'), KEY, {});
  return {
    turns: typeof raw.turns === 'number' ? raw.turns : 0,
    showAt: typeof raw.showAt === 'number' ? raw.showAt : FREE_CHATS,
    rated: !!raw.rated,
    reviews: Array.isArray(raw.reviews) ? raw.reviews.filter(isReview) : [],
  };
}

function isReview(value: unknown): value is Review {
  if (!value || typeof value !== 'object') return false;
  const v = value as Review;
  return typeof v.id === 'string' && typeof v.at === 'number' && typeof v.message === 'string';
}

function uid(): string {
  return globalThis.crypto?.randomUUID?.() ?? `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
}

export function githubIssueUrl(title: string, body: string): string {
  const url = new URL('https://github.com/Yash-Kavaiya/research-buddy/issues/new');
  url.searchParams.set('title', title.slice(0, 120));
  url.searchParams.set('body', body.slice(0, 4000));
  return url.toString();
}
