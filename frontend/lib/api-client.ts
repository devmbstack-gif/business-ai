import { API_BASE_URL } from "@/config/api";
import { getToken } from "@/lib/auth";

type ApiResponse<T> = {
  status: boolean;
  message: string;
  data: T;
};

type RequestOptions = {
  method?: string;
  body?: unknown;
  auth?: boolean;
};

export async function apiRequest<T>(
  path: string,
  options: RequestOptions = {}
): Promise<T> {
  const { method = "GET", body, auth = true } = options;

  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (auth) {
    const token = getToken();
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }
  }

  const response = await fetch(`${API_BASE_URL}${path}`, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined,
  });

  const json: ApiResponse<T> = await response.json();

  if (!response.ok || !json.status) {
    throw new Error(json.message || "Something went wrong");
  }

  return json.data;
}
