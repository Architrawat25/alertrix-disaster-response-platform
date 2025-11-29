"use client";

import { useEffect, useState } from "react";
import Image from "next/image";

export default function LoaderSplash() {
  const [show, setShow] = useState(true);

  useEffect(() => {
    const timer = setTimeout(() => setShow(false), 2500); // animation duration
    return () => clearTimeout(timer);
  }, []);

  if (!show) return null;

  return (
    <div className="fixed inset-0 z-[999] flex items-center justify-center bg-background animate-fadeOut">
      <Image
        src="/alertrix-logo.png"
        alt="Alertrix Logo"
        width={500}
        height={500}
        className="animate-zoomIn"
      />
    </div>
  );
}
