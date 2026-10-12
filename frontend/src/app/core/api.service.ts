import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, map, of, shareReplay } from 'rxjs';

import { KeyCheck, Provider, SkillCatalog, SkillDetail, Thumb } from './models';
import { SettingsStore } from './settings.store';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private readonly http = inject(HttpClient);
  private readonly settings = inject(SettingsStore);

  private catalog$?: Observable<SkillCatalog>;
  private providers$?: Observable<Provider[]>;

  catalog(): Observable<SkillCatalog> {
    this.catalog$ ??= this.http.get<SkillCatalog>('/api/skills').pipe(
      shareReplay({ bufferSize: 1, refCount: false }),
      catchError((error) => {
        this.catalog$ = undefined;
        throw error;
      }),
    );
    return this.catalog$;
  }

  skill(name: string): Observable<SkillDetail> {
    return this.http.get<SkillDetail>(`/api/skills/${encodeURIComponent(name)}`);
  }

  providers(): Observable<Provider[]> {
    this.providers$ ??= this.http.get<{ providers: Provider[] }>('/api/providers').pipe(
      map((r) => r.providers),
      shareReplay({ bufferSize: 1, refCount: false }),
      catchError((error) => {
        this.providers$ = undefined;
        throw error;
      }),
    );
    return this.providers$;
  }

  connectors(): Observable<Connector[]> {
    return this.http.get<{ connectors: Connector[] }>('/api/connectors').pipe(map((r) => r.connectors));
  }

  feedback(kind: Thumb | 'review', message: string, source: 'popup' | 'message' | 'support'): Observable<{ ok: boolean; message: string }> {
    return this.http.post<{ ok: boolean; message: string }>('/api/feedback', { kind, message, source });
  }

  validateKey(provider: string, model: string, key: string): Observable<KeyCheck> {
    return this.http
      .post<KeyCheck>('/api/keys/validate', null, {
        headers: this.settings.credentialHeaders(provider, model, key),
      })
      .pipe(catchError((error: HttpErrorResponse) => of({ ok: false, message: errorMessage(error) })));
  }
}

export interface Connector {
  id: string;
  name: string;
  detail: string;
  kind: 'builtin' | 'email' | 'key';
  header?: string;
  keyUrl?: string;
}

export function errorMessage(error: unknown): string {
  if (error instanceof HttpErrorResponse) {
    if (error.status === 0) return 'Could not reach the server. Check your connection.';
    return error.error?.message ?? `The server returned an error (${error.status}).`;
  }
  return error instanceof Error ? error.message : 'Something went wrong.';
}
