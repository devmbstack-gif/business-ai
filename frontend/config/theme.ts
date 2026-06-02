export const theme = {
  colors: {
    primary: "#31B772",
    primaryDark: "#1e7a4f",
    primaryLight: "#6FE09F",
    background: "#F7FBF9",
    surface: "#FFFFFF",
    text: "#0F172A",
    textMuted: "#64748B",
    border: "#E2E8F0",
    success: "#31B772",
    successLight: "#86EFAC",
    warning: "#EAB308",
    orange: "#F97316",
    danger: "#DC2626",
  },
  score: {
    excellent: "#16A34A",
    good: "#86EFAC",
    moderate: "#EAB308",
    low: "#F97316",
    poor: "#DC2626",
  },
};

export function getScoreColor(score: number | null | undefined): string {
  if (score == null) return theme.colors.textMuted;
  if (score >= 90) return theme.score.excellent;
  if (score >= 70) return theme.score.good;
  if (score >= 50) return theme.score.moderate;
  if (score >= 30) return theme.score.low;
  return theme.score.poor;
}
