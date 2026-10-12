export interface Stage {
  id: string;
  name: string;
  number: number;
}

export interface SkillSummary {
  name: string;
  description: string;
  stage: string;
  stageName: string;
  stageNumber: number;
  tags: string[];
  scripts: string[];
  hasScripts: boolean;
}

export interface SkillDetail extends SkillSummary {
  body: string;
  compatibility: string | null;
}

export interface SkillCatalog {
  stages: Stage[];
  skills: SkillSummary[];
}

export interface Provider {
  id: string;
  name: string;
  keyHint: string;
  keyUrl: string;
  models: string[];
}

export interface KeyCheck {
  ok: boolean;
  status?: number;
  message: string;
}

export interface Attachment {
  name: string;
  content: string;
  encoding: 'text' | 'base64';
}

export type ActivityStatus = 'running' | 'ok' | 'error';

export interface Activity {
  type: 'activity';
  id: string;
  kind: 'skill' | 'tool';
  name: string;
  label: string;
  detail?: string;
  status: ActivityStatus;
  preview?: string;
}

export interface TextBlock {
  type: 'text';
  text: string;
}

export type Block = TextBlock | Activity;

export interface Message {
  id: string;
  role: 'user' | 'assistant';
  blocks: Block[];
  pending?: boolean;
  error?: string;
  attachments?: string[];
}

export interface Conversation {
  id: string;
  title: string;
  skill: string | null;
  messages: Message[];
  updatedAt: number;
}

export type StreamEvent =
  | { type: 'text'; delta: string }
  | { type: 'skill_loaded'; id?: string; skill: string }
  | { type: 'tool_call'; id?: string; name: string; args: Record<string, unknown> }
  | { type: 'tool_result'; id?: string; name: string; ok: boolean; preview?: string }
  | { type: 'error'; status?: number; message: string }
  | { type: 'done' };

export function messageText(message: Message): string {
  return message.blocks
    .filter((b): b is TextBlock => b.type === 'text')
    .map((b) => b.text)
    .join('\n')
    .trim();
}
