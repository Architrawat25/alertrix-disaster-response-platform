import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';

type SeverityBadgeProps = {
  severity: number;
};

export default function SeverityBadge({ severity }: SeverityBadgeProps) {
  let severityClass = '';
  let severityLabel = 'Low';

  if (severity >= 70) {
    severityClass = 'bg-severity-high text-white hover:bg-severity-high/90';
    severityLabel = 'High';
  } else if (severity >= 40) {
    severityClass = 'bg-severity-medium text-black hover:bg-severity-medium/90';
    severityLabel = 'Medium';
  } else {
    severityClass = 'bg-severity-low text-white hover:bg-severity-low/90';
  }

  return (
    <Badge className={cn('font-bold', severityClass)}>
      {severityLabel} ({severity})
    </Badge>
  );
}
