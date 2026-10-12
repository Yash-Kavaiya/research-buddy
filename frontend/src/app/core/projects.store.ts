import { Injectable, effect, signal } from '@angular/core';

import { Project } from './models';
import { readJson, storage, writeJson } from './storage';

const KEY = 'rb.projects';

@Injectable({ providedIn: 'root' })
export class ProjectsStore {
  readonly projects = signal<Project[]>(sanitize(readJson(storage('local'), KEY, [])));

  constructor() {
    effect(() => writeJson(storage('local'), KEY, this.projects()));
  }

  create(name: string): Project | null {
    const title = name.trim().slice(0, 80);
    if (!title) return null;
    const project: Project = { id: uid(), name: title, createdAt: Date.now() };
    this.projects.update((list) => [project, ...list].slice(0, 40));
    return project;
  }

  rename(id: string, name: string): void {
    const title = name.trim().slice(0, 80);
    if (!title) return;
    this.projects.update((list) => list.map((p) => (p.id === id ? { ...p, name: title } : p)));
  }

  remove(id: string): void {
    this.projects.update((list) => list.filter((p) => p.id !== id));
  }
}

function uid(): string {
  return globalThis.crypto?.randomUUID?.() ?? `${Date.now().toString(36)}-${Math.random().toString(36).slice(2)}`;
}

function sanitize(value: unknown): Project[] {
  if (!Array.isArray(value)) return [];
  return value.filter(
    (p): p is Project => !!p && typeof p.id === 'string' && typeof p.name === 'string' && typeof p.createdAt === 'number',
  );
}
