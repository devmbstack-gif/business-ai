type BadgeProps = {
  children: React.ReactNode;
  variant?: "default" | "success" | "warning" | "danger" | "info" | "muted";
  className?: string;
};

const variants = {
  default: "bg-brand-secondary/10 text-brand-secondary",
  success: "bg-brand-success/10 text-brand-success",
  warning: "bg-brand-warning/10 text-brand-warning",
  danger: "bg-brand-danger/10 text-brand-danger",
  info: "bg-brand-accent/10 text-brand-accent",
  muted: "bg-brand-background text-brand-text-muted",
};

export function Badge({ children, variant = "default", className = "" }: BadgeProps) {
  return (
    <span
      className={`inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-medium ${variants[variant]} ${className}`}
    >
      {children}
    </span>
  );
}
