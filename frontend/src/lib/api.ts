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
    return {
      status: response.data.status === 'ok' ? 'ok' : 'unhealthy',
      database: response.data.database === 'connected' ? 'ok' : 'disconnected',
      mock_ai: response.data.ai_service === 'mock' ? 'ok' : 'disconnected'
    };
  } catch (error) {
    console.error('Failed to fetch health status:', error);
    return { status: 'unhealthy', database: 'disconnected', mock_ai: 'disconnected' };
  }
}

export async function fetchAlerts(): Promise<Alert[]> {
  try {
    const response = await apiClient.get<Alert[]>('/api/v1/alerts');
    return response.data.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  } catch (error) {
    console.error('Failed to fetch alerts:', error);
    return [];
  }
}

export async function postReport(report: Report): Promise<{ success: boolean; message: string }> {
  try {
    const response = await apiClient.post('/api/v1/report', report);
    return { success: true, message: 'Report received! Analysis in progress.' };
  } catch (error: any) {
    console.error('Failed to post report:', error);
    if (error.response) {
      return {
        success: false,
        message: `Failed to submit report: ${error.response.data.detail || error.message}`
      };
    }
    return { success: false, message: 'Network error: Cannot connect to server.' };
  }
}