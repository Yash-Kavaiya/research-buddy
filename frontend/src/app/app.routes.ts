import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', title: 'Research Buddy', loadComponent: () => import('./pages/home/home').then((m) => m.Home) },
  {
    path: 'skills',
    title: 'Skills · Research Buddy',
    loadComponent: () => import('./pages/skills/skills').then((m) => m.Skills),
  },
  {
    path: 'skills/:name',
    title: 'Skill · Research Buddy',
    loadComponent: () => import('./pages/skills/skill-detail').then((m) => m.SkillDetailPage),
  },
  {
    path: 'workspace',
    title: 'Workspace · Research Buddy',
    loadComponent: () => import('./pages/workspace/workspace').then((m) => m.Workspace),
  },
  {
    path: 'settings',
    title: 'Settings · Research Buddy',
    loadComponent: () => import('./pages/settings/settings').then((m) => m.Settings),
  },
  { path: '**', redirectTo: '' },
];
