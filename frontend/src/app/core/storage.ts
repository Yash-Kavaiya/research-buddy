/** JSON storage that never throws: private windows and blocked site data fall back to defaults. */

export function readJson<T>(store: Storage | null, key: string, fallback: T): T {
  try {
    const raw = store?.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

export function writeJson(store: Storage | null, key: string, value: unknown): boolean {
  try {
    store?.setItem(key, JSON.stringify(value));
    return true;
  } catch {
    return false;
  }
}

export function remove(store: Storage | null, key: string): void {
  try {
    store?.removeItem(key);
  } catch {
    /* nothing to remove */
  }
}

export function storage(kind: 'local' | 'session'): Storage | null {
  try {
    return kind === 'local' ? window.localStorage : window.sessionStorage;
  } catch {
    return null;
  }
}
