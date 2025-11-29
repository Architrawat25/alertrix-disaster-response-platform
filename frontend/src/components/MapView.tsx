'use client';

import { useEffect, useRef } from 'react';
import L from 'leaflet';
import type { Alert } from '@/lib/types';
import { format } from 'date-fns';

type MapViewProps = {
  alerts: Alert[];
};

const getSeverityStyles = (severity: number) => {
  if (severity >= 70) {
    return { color: 'hsl(0, 72%, 51%)', label: 'High' }; // Red
  }
  if (severity >= 40) {
    return { color: 'hsl(48, 96%, 53%)', label: 'Medium' }; // Yellow
  }
  return { color: 'hsl(142, 64%, 42%)', label: 'Low' }; // Green
};

const createDivIcon = (color: string) => {
    return L.divIcon({
      html: `<span style="background-color: ${color}; width: 1.5rem; height: 1.5rem; border-radius: 50%; display: flex; justify-content: center; align-items: center; border: 2px solid white; box-shadow: 0 2px 5px rgba(0,0,0,0.3);"><span style="background-color: white; width: 0.5rem; height: 0.5rem; border-radius: 50%;"></span></span>`,
      className: '',
      iconSize: [24, 24],
      iconAnchor: [12, 12],
    });
};

export default function MapView({ alerts }: MapViewProps) {
  const mapRef = useRef<HTMLDivElement>(null);
  const mapInstanceRef = useRef<L.Map | null>(null);

  useEffect(() => {
    if (mapRef.current && !mapInstanceRef.current) {
      const map = L.map(mapRef.current).setView([20, 0], 2);
      mapInstanceRef.current = map;

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors',
      }).addTo(map);
    }
  }, []);

  useEffect(() => {
    const map = mapInstanceRef.current;
    if (!map) return;
    
    // Clear existing markers
    map.eachLayer(layer => {
      if (layer instanceof L.Marker) {
        map.removeLayer(layer);
      }
    });

    if (alerts.length === 0) return;

    const markers = L.featureGroup();

    alerts.forEach(alert => {
      const { color, label } = getSeverityStyles(alert.severity);
      const marker = L.marker([alert.lat, alert.lon], {
        icon: createDivIcon(color),
      });

      const popupContent = `
        <div style="font-family: Inter, sans-serif; font-size: 14px; line-height: 1.6;">
          <h3 style="font-weight: 600; font-size: 16px; margin: 0 0 8px; color: #2E4765;">${alert.alert_type}</h3>
          <p style="margin: 0 0 4px;"><strong>Summary:</strong> ${alert.summary}</p>
          <p style="margin: 0 0 4px;"><strong>Location:</strong> ${alert.location}</p>
          <p style="margin: 0 0 4px;"><strong>Severity:</strong> <span style="color: ${color}; font-weight: bold;">${label} (${alert.severity})</span></p>
          <p style="margin: 0; font-size: 12px; color: #666;">${format(new Date(alert.timestamp), 'PPpp')}</p>
        </div>
      `;

      marker.bindPopup(popupContent);
      markers.addLayer(marker);
    });

    markers.addTo(map);

    if (markers.getLayers().length > 0) {
        map.fitBounds(markers.getBounds().pad(0.2));
    }
  }, [alerts]);

  return <div ref={mapRef} className="h-full w-full z-0" />;
}
