export const theme = {
  colors: {
    primary: "#001B3D",
    secondary: "#0070F3",
    accent: "#00C2FF",
    background: "#F4F7FB",
    surface: "#FFFFFF",
    text: "#001B3D",
    textMuted: "#64748B",
    border: "#E2E8F0",
    success: "#16A34A",
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
