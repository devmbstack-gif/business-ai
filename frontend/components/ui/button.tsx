import { ButtonHTMLAttributes } from "react";

type ButtonProps = ButtonHTMLAttributes<HTMLButtonElement> & {
  variant?: "primary" | "secondary" | "outline" | "ghost" | "danger";
  size?: "sm" | "md" | "lg";
  loading?: boolean;
};

const variants = {
  primary: "gradient-primary text-white hover:brightness-110 active:scale-[0.98] shadow-sm",
  secondary: "bg-brand-primary-dark text-white hover:brightness-110 active:scale-[0.98]",
  outline: "border border-brand-border bg-brand-surface text-slate-700 hover:bg-slate-50 hover:border-slate-300",
  ghost: "text-brand-text-muted hover:bg-slate-100 hover:text-brand-text",
  danger: "bg-brand-danger text-white hover:brightness-110",
};

const sizes = {
  sm: "px-3 py-1.5 text-sm rounded-lg",
  md: "px-4 py-2.5 text-sm rounded-xl",
  lg: "px-6 py-3.5 text-sm rounded-xl",
};

export function Button({
  variant = "primary",
  size = "md",
  loading,
  className = "",
  children,
  disabled,
  ...props
}: ButtonProps) {
  return (
    <button
      className={`inline-flex items-center justify-center gap-2 font-semibold transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:active:scale-100 ${variants[variant]} ${sizes[size]} ${className}`}
      disabled={disabled || loading}
      {...props}
    >
      {loading && (
        <span className="h-4 w-4 animate-spin rounded-full border-2 border-white border-t-transparent" />
      )}
      {children}
    </button>
  );
}
