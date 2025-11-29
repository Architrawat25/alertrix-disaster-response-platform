'use client';

import { useState, useEffect, useMemo } from 'react';
import { AlertCircle, BarChart, CheckCircle, ChevronRight, Filter, Link as LinkIcon, Server, ShieldAlert, XCircle } from 'lucide-react';
import Link from 'next/link';

import { checkHealth, fetchAlerts } from '@/lib/api';
import type { Alert as AlertType, HealthStatus } from '@/lib/types';
import AlertList from '@/components/AlertList';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Separator } from '@/components/ui/separator';
import { Checkbox } from '@/components/ui/checkbox';
import { Label } from '@/components/ui/label';
import { Skeleton } from '@/components/ui/skeleton';

type SeverityFilters = {
  low: boolean;
  medium: boolean;
  high: boolean;
};

function getSeverityCategory(severity: number): keyof SeverityFilters {
  if (severity < 40) return 'low';
  if (severity < 70) return 'medium';
  return 'high';
}

export default function Home() {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [alerts, setAlerts] = useState<AlertType[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<SeverityFilters>({
    low: true,
    medium: true,
    high: true,
  });

  useEffect(() => {
    const loadData = async () => {
      setLoading(true);
      const [healthData, alertsData] = await Promise.all([checkHealth(), fetchAlerts()]);
      setHealth(healthData);
      setAlerts(alertsData);
      setLoading(false);
    };

    loadData();

    const intervalId = setInterval(async () => {
      const alertsData = await fetchAlerts();
      setAlerts(alertsData);
    }, 30000); // Refresh every 30 seconds

    return () => clearInterval(intervalId);
  }, []);

  const filteredAlerts = useMemo(() => {
    return alerts.filter(alert => {
      const severityCategory = getSeverityCategory(alert.severity);
      return filters[severityCategory];
    });
  }, [alerts, filters]);

  const alertStats = useMemo(() => {
    return alerts.reduce(
      (acc, alert) => {
        const category = getSeverityCategory(alert.severity);
        acc[category]++;
        acc.total++;
        return acc;
      },
      { low: 0, medium: 0, high: 0, total: 0 }
    );
  }, [alerts]);

  const handleFilterChange = (filterName: keyof SeverityFilters) => {
    setFilters(prev => ({ ...prev, [filterName]: !prev[filterName] }));
  };

  const HealthStatusIndicator = ({ status, name }: { status: 'ok' | 'unhealthy' | 'disconnected' | string; name: string }) => {
    const isOk = status === 'ok';
    return (
      <div className="flex items-center gap-2">
        {isOk ? <CheckCircle className="h-5 w-5 text-green-500" /> : <XCircle className="h-5 w-5 text-red-500" />}
        <span className="text-sm">
          {name}: <span className={`font-semibold ${isOk ? 'text-green-600 dark:text-green-400' : 'text-red-600 dark:text-red-400'}`}>{status}</span>
        </span>
      </div>
    );
  };

  return (
    <div className="container mx-auto max-w-7xl p-4 sm:p-6 lg:p-8">
      <div className="space-y-6">
        <header className="space-y-2">
          <h1 className="text-3xl font-bold tracking-tight">Dashboard</h1>
          <p className="text-muted-foreground">
            Overview of system status and current disaster alerts. Data refreshes periodically.
          </p>
        </header>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
          <Card>
            <CardHeader>
              <CardTitle className="text-base font-medium">System Health</CardTitle>
            </CardHeader>
            <CardContent className="space-y-2">
              {loading ? (
                <div className="space-y-3">
                  <Skeleton className="h-5 w-3/4" />
                  <Skeleton className="h-5 w-2/3" />
                  <Skeleton className="h-5 w-1/2" />
                </div>
              ) : (
                health && (
                  <>
                    <HealthStatusIndicator status={health.status} name="API Status" />
                    <HealthStatusIndicator status={health.database} name="Database" />
                    <HealthStatusIndicator status={health.mock_ai} name="AI Service" />
                  </>
                )
              )}
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">Total Alerts</CardTitle>
              <AlertCircle className="h-4 w-4 text-muted-foreground" />
            </CardHeader>
            <CardContent>
              {loading ? <Skeleton className="h-8 w-1/2" /> : <div className="text-2xl font-bold">{alertStats.total}</div>}
            </CardContent>
          </Card>
          <Card>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium">High Severity</CardTitle>
              <ShieldAlert className="h-4 w-4 text-destructive" />
            </CardHeader>
            <CardContent>
              {loading ? <Skeleton className="h-8 w-1/2" /> : <div className="text-2xl font-bold text-destructive">{alertStats.high}</div>}
            </CardContent>
          </Card>
          <Card className="lg:col-span-2 md:col-span-2">
            <CardHeader>
              <CardTitle className="text-base font-medium">Quick Actions</CardTitle>
            </CardHeader>
            <CardContent className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <Button asChild size="lg" className="justify-between">
                <Link href="/map">
                  <span>View on Map</span>
                  <BarChart />
                </Link>
              </Button>
              <Button asChild size="lg" variant="secondary" className="justify-between">
                <Link href="/reports">
                  <span>Report Incident</span>
                  <ChevronRight />
                </Link>
              </Button>
            </CardContent>
          </Card>
        </div>

        <div>
          <Card>
            <CardHeader>
              <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                <CardTitle>Current Alerts</CardTitle>
                <div className="flex items-center gap-4 text-sm">
                  <div className="flex items-center gap-2 font-medium">
                    <Filter className="h-4 w-4" />
                    <span>Filter by severity:</span>
                  </div>
                  <div className="flex items-center space-x-4">
                      {(['low', 'medium', 'high'] as const).map((sev) => (
                        <div key={sev} className="flex items-center space-x-2">
                          <Checkbox
                            id={`filter-${sev}`}
                            checked={filters[sev]}
                            onCheckedChange={() => handleFilterChange(sev)}
                          />
                          <Label htmlFor={`filter-${sev}`} className="capitalize">
                            {sev}
                          </Label>
                        </div>
                      ))}
                  </div>
                </div>
              </div>
            </CardHeader>
            <CardContent>
              <Separator className="mb-4" />
              {loading ? <Skeleton className="h-96 w-full" /> : <AlertList alerts={filteredAlerts} />}
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
