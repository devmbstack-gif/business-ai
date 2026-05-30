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
    <Card className={accent ? "border-brand-secondary/20" : ""}>
      <CardBody className="flex items-start justify-between">
        <div>
          <p className="text-sm font-medium text-brand-text-muted">{title}</p>
          <p className={`mt-2 text-3xl font-bold ${accent ? "gradient-text" : "text-brand-text"}`}>
            {value}
          </p>
          {subtitle && (
            <p className="mt-1 text-xs text-brand-text-muted">{subtitle}</p>
          )}
        </div>
        {icon && (
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-secondary/10 text-brand-secondary">
            {icon}
          </div>
        )}
      </CardBody>
    </Card>
  );
}
