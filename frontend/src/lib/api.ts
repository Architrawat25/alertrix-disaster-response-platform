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
    const response = await apiClient.get<HealthStatus>('/health');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch health status:', error);
    // Return a default unhealthy status on error
    return { status: 'unhealthy', database: 'disconnected', mock_ai: 'disconnected' };
  }
}

export async function fetchAlerts(): Promise<Alert[]> {
  try {
    const response = await apiClient.get<Alert[]>('/alerts');
    // Sort by timestamp descending
    return response.data.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
  } catch (error) {
    console.error('Failed to fetch alerts:', error);
    return [];
  }
}

export async function postReport(report: Report): Promise<{ success: boolean; message: string }> {
  try {
    await apiClient.post('/report', report);
    return { success: true, message: 'Report received! Analysis in progress.' };
  } catch (error) {
    console.error('Failed to post report:', error);
    if (axios.isAxiosError(error) && error.response) {
      return { success: false, message: `Failed to submit report: ${error.response.data.detail || error.message}` };
    }
    return { success: false, message: 'An unknown error occurred while submitting the report.' };
  }
}
