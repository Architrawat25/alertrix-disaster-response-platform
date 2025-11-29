import Image from 'next/image';

export default function Footer() {
  return (
    <footer className="border-t bg-background">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        
        {/* LOGO + TEXT */}
        <div className="flex items-center gap-2">
          <Image
            src="/alertrix-logo.png"
            alt="Alertrix Logo"
            width={20}
            height={20}
            className="rounded-sm"
          />
          <p className="text-sm text-muted-foreground">
            &copy; {new Date().getFullYear()} Alertrix. All rights reserved.
          </p>
        </div>

        <p className="text-sm text-muted-foreground">
          AI-Integrated Disaster Management
        </p>
      </div>
    </footer>
  );
}
