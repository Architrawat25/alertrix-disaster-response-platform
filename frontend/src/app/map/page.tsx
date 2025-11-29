"use client";

import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import { fetchAlerts } from "@/lib/api";
import type { Alert } from "@/lib/types";
import { Skeleton } from "@/components/ui/skeleton";

// Skeleton for loading state
const MapSkeleton = () => (
  <div className="h-full w-full bg-muted">
    <div className="flex items-center justify-center h-full">
      <div className="text-center space-y-2">
        <Skeleton className="h-8 w-32 mx-auto" />
        <Skeleton className="h-4 w-48" />
      </div>
    </div>
  </div>
);

// Dynamic import of MapView so Leaflet loads only on client
const MapView = dynamic(() => import("@/components/MapView"), {
  ssr: false,
  loading: () => <MapSkeleton />,
});

export default function MapPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      try {
        const data = await fetchAlerts();
        setAlerts(data);
      } catch (error) {
        console.error("Failed to fetch alerts:", error);
      } finally {
        setLoading(false);
      }
    }

    loadData();
  }, []);

  return (
    <div className="flex flex-col" style={{ height: "calc(100vh - 4rem)" }}>
      {loading ? <MapSkeleton /> : <MapView alerts={alerts} />}
    </div>
  );
}
