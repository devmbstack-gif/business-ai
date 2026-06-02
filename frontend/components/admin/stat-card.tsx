import { Card, CardBody } from "@/components/ui/card";

type StatCardProps = {
  title: string;
  value: string | number;
  subtitle?: string;
  icon?: React.ReactNode;
  accent?: boolean;
};

export function StatCard({ title, value, subtitle, icon, accent }: StatCardProps) {
  return (
    <Card className={`transition-shadow hover:shadow-md ${accent ? "border-brand-primary/25 bg-gradient-to-br from-brand-surface to-brand-primary/5" : ""}`}>
      <CardBody className="flex items-start justify-between p-5">
        <div>
          <p className="text-sm font-medium text-brand-text-muted">{title}</p>
          <p className={`mt-2 text-3xl font-bold tracking-tight ${accent ? "gradient-text" : "text-slate-900"}`}>
            {value}
          </p>
          {subtitle && (
            <p className="mt-1 text-xs text-brand-text-muted">{subtitle}</p>
          )}
        </div>
        {icon && (
          <div className="flex h-11 w-11 items-center justify-center rounded-xl bg-brand-primary/10 text-brand-primary">
            {icon}
          </div>
        )}
      </CardBody>
    </Card>
  );
}
