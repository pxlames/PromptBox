let BASE_URL: string = 'http://127.0.0.1:8000';
let resolveReady: (() => void) | null = null;
// 当配置读取完成后 resolve，用于首屏请求等待配置
const configReady: Promise<void> = new Promise((resolve) => { resolveReady = resolve; });

// runtime config via /public/config.json
// if the file exists, override BASE_URL at runtime
fetch('/config.json').then(async (r) => {
  try {
    if (r.ok) {
      const cfg = await r.json();
      if (cfg && typeof cfg.apiBase === 'string' && cfg.apiBase.trim()) {
        BASE_URL = cfg.apiBase.trim();
      }
    }
  } catch {}
  finally { if (resolveReady) resolveReady(); }
}).catch(() => { if (resolveReady) resolveReady(); });

export type Prompt = {
  id: number;
  title: string;
  content: string;
  tags?: string;
  created_at: string;
  updated_at: string;
};

export type PromptCreate = Omit<Prompt, 'id' | 'created_at' | 'updated_at'>;
export type PromptUpdate = Partial<PromptCreate>;

async function http<T>(path: string, init?: RequestInit): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...init,
  });
  if (!res.ok) {
    const text = await res.text();
    throw new Error(text || res.statusText);
  }
  if (res.status === 204) return undefined as unknown as T;
  return (await res.json()) as T;
}

export const api = {
  ready: () => configReady,
  list: (params?: { skip?: number; limit?: number; q?: string | null; sort?: string | null }) => {
    const query = new URLSearchParams();
    if (params?.skip != null) query.set('skip', String(params.skip));
    if (params?.limit != null) query.set('limit', String(params.limit));
    if (params?.q) query.set('q', params.q);
    if (params?.sort) query.set('sort', params.sort);
    const qs = query.toString();
    return http<Prompt[]>(`/prompts/${qs ? `?${qs}` : ''}`);
  },
  count: (q?: string | null) => {
    const query = new URLSearchParams();
    if (q) query.set('q', q);
    const qs = query.toString();
    return http<{ total: number }>(`/prompts/count${qs ? `?${qs}` : ''}`);
  },
  get: (id: number) => http<Prompt>(`/prompts/${id}`),
  create: (data: PromptCreate) => http<Prompt>('/prompts/', { method: 'POST', body: JSON.stringify(data) }),
  update: (id: number, data: PromptUpdate) => http<Prompt>(`/prompts/${id}`, { method: 'PUT', body: JSON.stringify(data) }),
  remove: (id: number) => http<void>(`/prompts/${id}`, { method: 'DELETE' }),
};


