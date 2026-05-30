import { getScoreColor } from "@/config/theme";

type ScoreBadgeProps = {
  score: number | null | undefined;
};

export function ScoreBadge({ score }: ScoreBadgeProps) {
  if (score == null) {
    return <span className="text-sm text-brand-text-muted">N/A</span>;
  }

  const color = getScoreColor(score);

  return (
    <span
      className="inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold"
      style={{ backgroundColor: `${color}20`, color }}
    >
      {score.toFixed(0)}
    </span>
  );
}
