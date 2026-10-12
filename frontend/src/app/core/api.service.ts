import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Injectable, inject } from '@angular/core';
import { Observable, catchError, map, of, shareReplay } from 'rxjs';

import { KeyCheck, Provider, SkillCatalog, SkillDetail } from './models';
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
        this.catalog$ = undefined; // let the next caller retry
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

  /** The chat models this key can use, asked from the provider itself. */
  models(provider: string, key: string): Observable<string[]> {
    return this.http
      .get<{ models: string[] }>('/api/models', { headers: { 'X-LLM-Provider': provider, 'X-LLM-Key': key } })
      .pipe(map((r) => r.models));
  }

  validateKey(provider: string, model: string, key: string): Observable<KeyCheck> {
    return this.http
      .post<KeyCheck>('/api/keys/validate', null, { headers: this.settings.credentialHeaders(provider, model, key) })
      .pipe(catchError((error: HttpErrorResponse) => of({ ok: false, message: errorMessage(error) })));
  }
}

export function errorMessage(error: unknown): string {
  if (error instanceof HttpErrorResponse) {
    if (error.status === 0) return 'Could not reach the server. Check your connection.';
    return error.error?.message ?? `The server returned an error (${error.status}).`;
  }
  return error instanceof Error ? error.message : 'Something went wrong.';
}
