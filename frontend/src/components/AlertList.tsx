import type { Alert as AlertType } from '@/lib/types';
import { ScrollArea } from '@/components/ui/scroll-area';
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from '@/components/ui/table';
import SeverityBadge from './SeverityBadge';
import { format } from 'date-fns';
import { AlertTriangle, MapPin, Tag } from 'lucide-react';

type AlertListProps = {
  alerts: AlertType[];
};

export default function AlertList({ alerts }: AlertListProps) {
  if (alerts.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center gap-4 rounded-md border border-dashed p-8 text-center h-96">
        <div className="flex h-20 w-20 items-center justify-center rounded-full bg-secondary">
          <AlertTriangle className="h-10 w-10 text-muted-foreground" />
        </div>
        <h2 className="text-xl font-semibold">No Alerts Found</h2>
        <p className="text-muted-foreground">There are currently no alerts matching your criteria.</p>
      </div>
    );
  }

  return (
    <ScrollArea className="h-96 rounded-md border">
      <Table>
        <TableHeader className="sticky top-0 bg-secondary">
          <TableRow>
            <TableHead>Severity</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Location</TableHead>
            <TableHead className="text-right">Timestamp</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {alerts.map(alert => (
            <TableRow key={alert.id}>
              <TableCell>
                <SeverityBadge severity={alert.severity} />
              </TableCell>
              <TableCell className="font-medium">
                <div className="flex items-center gap-2">
                  <Tag className="w-4 h-4 text-muted-foreground" />
                  <span>{alert.alert_type}</span>
                </div>
              </TableCell>
              <TableCell>
                <div className="flex items-center gap-2">
                  <MapPin className="w-4 h-4 text-muted-foreground" />
                  <span>{alert.location}</span>
                </div>
              </TableCell>
              <TableCell className="text-right text-muted-foreground">
                {format(new Date(alert.timestamp), 'PPpp')}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </ScrollArea>
  );
}
