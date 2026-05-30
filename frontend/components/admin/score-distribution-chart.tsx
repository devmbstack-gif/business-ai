import { ScoreDistributionItem } from "@/types/admin";

type ScoreDistributionChartProps = {
  data: ScoreDistributionItem[];
};

const barColors = [
  "bg-brand-success",
  "bg-brand-success-light",
  "bg-brand-warning",
  "bg-brand-orange",
  "bg-brand-danger",
];

export function ScoreDistributionChart({ data }: ScoreDistributionChartProps) {
  if (data.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-brand-text-muted">No score data yet</p>
    );
  }

  return (
    <div className="space-y-3">
      {data.map((item, index) => (
        <div key={item.range_label}>
          <div className="mb-1 flex items-center justify-between text-sm">
            <span className="text-brand-text">{item.range_label}</span>
            <span className="text-brand-text-muted">
              {item.count} ({item.percentage.toFixed(1)}%)
            </span>
          </div>
          <div className="h-2.5 overflow-hidden rounded-full bg-brand-background">
            <div
              className={`h-full rounded-full transition-all ${barColors[index % barColors.length]}`}
              style={{ width: `${Math.max(item.percentage, 2)}%` }}
            />
          </div>
        </div>
      ))}
    </div>
  );
}
