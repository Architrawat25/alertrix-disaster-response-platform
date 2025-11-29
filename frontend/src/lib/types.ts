export interface Alert {
  id: number;
  alert_type: string;
  summary: string;
  location: string;
  lat: number;
  lon: number;
  severity: number;
  timestamp: string;
  source: string;
}

export interface Report {
  text: string;
  lat: number;
  lon: number;
  source: string;
}

export interface HealthStatus {
  status: 'ok' | 'unhealthy';
  database: 'ok' | 'disconnected';
  mock_ai: 'ok' | 'disconnected';
}
