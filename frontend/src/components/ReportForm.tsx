'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import * as z from 'zod';
import { Button } from '@/components/ui/button';
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from '@/components/ui/form';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { useToast } from '@/hooks/use-toast';
import { postReport } from '@/lib/api';
import { Loader2 } from 'lucide-react';

const reportFormSchema = z.object({
  text: z.string().min(10, 'Description must be at least 10 characters long.'),
  lat: z.coerce.number().min(-90, 'Latitude must be between -90 and 90.').max(90, 'Latitude must be between -90 and 90.'),
  lon: z.coerce.number().min(-180, 'Longitude must be between -180 and 180.').max(180, 'Longitude must be between -180 and 180.'),
  source: z.string().min(2, 'Source must be at least 2 characters long.'),
});

type ReportFormValues = z.infer<typeof reportFormSchema>;

export default function ReportForm() {
  const { toast } = useToast();
  const form = useForm<ReportFormValues>({
    resolver: zodResolver(reportFormSchema),
    defaultValues: {
      text: '',
      source: 'WebApp User',
    },
  });

  const { isSubmitting } = form.formState;

  async function onSubmit(values: ReportFormValues) {
    try {
      const backendResult = await postReport(values);
  
      if (backendResult.success) {
        toast({
          title: 'Report Submitted Successfully',
          description: 'Report received! Analysis in progress.',
        });
  
        form.reset();
      } else {
        toast({
          title: 'Submission Failed',
          description: backendResult.message ?? 'Error submitting report.',
          variant: 'destructive',
        });
      }
    } catch (error) {
      toast({
        title: 'Submission Error',
        description: 'Could not submit report. Please try again.',
        variant: 'destructive',
      });
    }
  }
  

  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
        <FormField
          control={form.control}
          name="text"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Incident Description</FormLabel>
              <FormControl>
                <Textarea placeholder="Describe the incident in detail..." {...field} rows={5} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <FormField
            control={form.control}
            name="lat"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Latitude</FormLabel>
                <FormControl>
                  <Input type="number" step="any" placeholder="e.g., 34.0522" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <FormField
            control={form.control}
            name="lon"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Longitude</FormLabel>
                <FormControl>
                  <Input type="number" step="any" placeholder="e.g., -118.2437" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
        </div>
        <FormField
          control={form.control}
          name="source"
          render={({ field }) => (
            <FormItem>
              <FormLabel>Source</FormLabel>
              <FormControl>
                <Input placeholder="e.g., Local Observer" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" disabled={isSubmitting} className="w-full">
          {isSubmitting && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
          Submit Report
        </Button>
      </form>
    </Form>
  );
}
