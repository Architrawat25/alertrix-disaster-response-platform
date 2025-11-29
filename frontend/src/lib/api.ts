import axios from 'axios';
import type { Alert, Report, HealthStatus } from '@/lib/types';

export const API_BASE = process.env.NEXT_PUBLIC_API_BASE;

const apiClient = axios.create({
  baseURL: API_BASE,
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function checkHealth(): Promise<HealthStatus> {
  try {
    const response = await apiClient.get<any>('/health');
    // Map the backend response to frontend expected format
    return { 
      status: response.data.status || 'unknown', 
      database: 'connected', // We'll assume connected if health check passes
      mock_ai: 'connected'   // Same for AI service
    };
  } catch (error) {
    console.error('Failed to fetch health status:', error);
    return { status: 'unhealthy', database: 'disconnected', mock_ai: 'disconnected' };
  }
}

export async function fetchAlerts(): Promise<Alert[]> {
  try {
    const response = await apiClient.get<Alert[]>('/api/v1/alerts');
    // Map backend fields to frontend expected fields
    const alerts = response.data.map(alert => ({
      ...alert,
      // If frontend expects 'timestamp' but backend uses 'created_at'
      timestamp: alert.created_at || alert.timestamp
    }));
    // Sort by timestamp descending
    return alerts.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  } catch (error) {
    console.error('Failed to fetch alerts:', error);
    return [];
  }
}

export async function postReport(report: Report): Promise<{ success: boolean; message: string }> {
  try {
    // Use the correct endpoint with /api/v1 prefix
    await apiClient.post('/api/v1/report', report);
    return { success: true, message: 'Report received! Analysis in progress.' };
  } catch (error) {
    console.error('Failed to post report:', error);
    if (axios.isAxiosError(error) && error.response) {
      return { success: false, message: `Failed to submit report: ${error.response.data.detail || error.message}` };
    }
    return { success: false, message: 'An unknown error occurred while submitting the report.' };
  }
}
