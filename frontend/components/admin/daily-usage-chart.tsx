import { DailyUsageItem } from "@/types/admin";

type DailyUsageChartProps = {
  data: DailyUsageItem[];
};

export function DailyUsageChart({ data }: DailyUsageChartProps) {
  if (data.length === 0) {
    return (
      <p className="py-8 text-center text-sm text-brand-text-muted">No usage data yet</p>
    );
  }

  const maxValue = Math.max(
    ...data.map((d) => Math.max(d.analyses_count, d.proposals_count)),
    1
  );

  return (
    <div className="flex items-end justify-between gap-3 pt-4" style={{ height: 180 }}>
      {data.map((item) => {
        const analysisHeight = (item.analyses_count / maxValue) * 100;
        const proposalHeight = (item.proposals_count / maxValue) * 100;
        const dateLabel = new Date(item.date).toLocaleDateString("en-US", {
          weekday: "short",
        });

        return (
          <div key={item.date} className="flex flex-1 flex-col items-center gap-2">
            <div className="flex w-full items-end justify-center gap-1" style={{ height: 140 }}>
              <div
                className="w-3 rounded-t bg-brand-primary transition-all"
                style={{ height: `${analysisHeight}%`, minHeight: item.analyses_count > 0 ? 4 : 0 }}
                title={`Analyses: ${item.analyses_count}`}
              />
              <div
                className="w-3 rounded-t bg-brand-primary-light transition-all"
                style={{ height: `${proposalHeight}%`, minHeight: item.proposals_count > 0 ? 4 : 0 }}
                title={`Proposals: ${item.proposals_count}`}
              />
            </div>
            <span className="text-[10px] text-brand-text-muted">{dateLabel}</span>
          </div>
        );
      })}
    </div>
  );
}
