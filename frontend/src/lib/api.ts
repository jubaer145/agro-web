// API Client with centralized error handling and base URL configuration

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

interface FetchOptions extends RequestInit {
  params?: Record<string, string>;
}

class APIError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = 'APIError';
  }
}

async function apiClient<T>(endpoint: string, options: FetchOptions = {}): Promise<T> {
  const { params, ...fetchOptions } = options;
  
  // Build URL with query parameters
  let url = `${API_BASE_URL}${endpoint}`;
  if (params) {
    const searchParams = new URLSearchParams();
    Object.entries(params).forEach(([key, value]) => {
      if (value) searchParams.append(key, value);
    });
    const queryString = searchParams.toString();
    if (queryString) url += `?${queryString}`;
  }
  
  try {
    const response = await fetch(url, {
      ...fetchOptions,
      headers: {
        'Content-Type': 'application/json',
        ...fetchOptions.headers,
      },
    });
    
    if (!response.ok) {
      throw new APIError(
        response.status,
        `API Error: ${response.status} ${response.statusText}`
      );
    }
    
    return await response.json();
  } catch (error) {
    if (error instanceof APIError) {
      throw error;
    }
    throw new APIError(0, `Network Error: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

export const api = {
  // Generic methods
  get: <T>(endpoint: string, params?: Record<string, string>) =>
    apiClient<T>(endpoint, { method: 'GET', params }),
  
  post: <T>(endpoint: string, data: unknown) =>
    apiClient<T>(endpoint, { method: 'POST', body: JSON.stringify(data) }),
  
  patch: <T>(endpoint: string, data: unknown) =>
    apiClient<T>(endpoint, { method: 'PATCH', body: JSON.stringify(data) }),
  
  delete: <T>(endpoint: string) =>
    apiClient<T>(endpoint, { method: 'DELETE' }),
  
  // Specific endpoints
  districts: () => api.get<any>('/api/districts/'),
  
  farms: (params?: { district?: string; search?: string }) =>
    api.get<any>('/api/farms/', params),
  
  events: (params?: { district?: string; event_type?: string; status?: string }) =>
    api.get<any>('/api/events/', params),
  
  updateEventStatus: (id: number, status: string) =>
    api.patch<any>(`/api/events/${id}/`, { status }),
  
  cropIssues: (params?: { district?: string; crop_type?: string; problem_type?: string; severity?: string; status?: string }) =>
    api.get<any>('/api/crop-issues/', params),
  
  updateCropIssueStatus: (id: number, status: string) =>
    api.patch<any>(`/api/crop-issues/${id}/`, { status }),
  
  dashboardSummary: (district?: string) =>
    api.get<any>('/api/dashboard/summary/', district ? { district } : undefined),
};

export { APIError };
