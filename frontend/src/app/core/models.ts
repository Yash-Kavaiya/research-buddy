export interface Stage {
  index: number;
  name: string;
  count: number;
}

export interface SkillBrief {
  name: string;
  title: string;
  description: string;
  summary: string;
  stage: string;
  stage_index: number;
  tags: string[];
  scripts: string[];
}

export interface SkillDetail extends SkillBrief {
  references: string[];
  markdown: string;
}

export interface SkillCatalog {
  stages: Stage[];
  skills: SkillBrief[];
}

export interface Provider {
  id: string;
  name: string;
  key_hint: string;
  key_url: string;
}

export interface KeyCheck {
  ok: boolean;
  message: string;
  status?: number;
}

/** One step the agent took while answering: a skill it loaded or a tool it ran. */
export interface Activity {
  type: 'activity';
  id: string;
  kind: 'skill' | 'tool';
  name: string;
  label: string;
  detail?: string;
  status: 'running' | 'ok' | 'error';
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
  attachments?: string[];
  error?: string;
  /** True while the answer is still streaming. Never persisted as true. */
  pending?: boolean;
}

export interface Conversation {
  id: string;
  title: string;
  skill: string | null;
  messages: Message[];
  updatedAt: number;
}

export interface Attachment {
  name: string;
  content: string;
  encoding: 'text' | 'base64';
  size: number;
}

/** Events sent by POST /api/chat. */
export type StreamEvent =
  | { type: 'text'; delta: string }
  | { type: 'skill_loaded'; id: string; skill: string }
  | { type: 'tool_call'; id: string; name: string; args: Record<string, unknown> }
  | { type: 'tool_result'; id: string; name: string; ok: boolean; preview: string }
  | { type: 'error'; message: string; status?: number }
  | { type: 'done' };

export function messageText(message: Message): string {
  return message.blocks
    .filter((b): b is TextBlock => b.type === 'text')
    .map((b) => b.text)
    .join('\n\n')
    .trim();
}
