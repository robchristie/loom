type ApiErrorShape = { detail?: unknown };

function readBase(): string {
  // For dev: use relative "/api" so Vite proxy works.
  // If you later host UI separately, you can switch to a full base URL here.
  return '';
}

export function apiUrl(path: string): string {
  const base = readBase();
  if (!path.startsWith('/')) path = '/' + path;
  return base ? base.replace(/\/+$/, '') + path : path;
}

async function parseError(res: Response): Promise<string> {
  const ct = res.headers.get('content-type') ?? '';
  try {
    if (ct.includes('application/json')) {
      const body = (await res.json()) as ApiErrorShape;
      if (typeof body.detail === 'string') return body.detail;
      return JSON.stringify(body);
    }
    return await res.text();
  } catch {
    return `${res.status} ${res.statusText}`;
  }
}

export async function apiGet<T>(path: string): Promise<T> {
  const res = await fetch(apiUrl(path));
  if (!res.ok) throw new Error(await parseError(res));
  return (await res.json()) as T;
}

export async function apiGetOrNull<T>(path: string): Promise<T | null> {
  try {
    return await apiGet<T>(path);
  } catch {
    return null;
  }
}

export async function apiPost<T>(path: string, body?: unknown): Promise<T> {
  const init: RequestInit = {
    method: 'POST',
    headers: {}
  };

  if (body !== undefined) {
    init.headers = { 'content-type': 'application/json' };
    init.body = JSON.stringify(body);
  }

  const res = await fetch(apiUrl(path), init);
  if (!res.ok) throw new Error(await parseError(res));

  // Some endpoints might return empty; treat as null json if needed
  const ct = res.headers.get('content-type') ?? '';
  if (!ct.includes('application/json')) return (null as unknown) as T;
  return (await res.json()) as T;
}

