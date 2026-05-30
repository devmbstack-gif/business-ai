import { InputHTMLAttributes } from "react";

type InputProps = InputHTMLAttributes<HTMLInputElement> & {
  label?: string;
  error?: string;
};

export function Input({ label, error, className = "", id, ...props }: InputProps) {
  const inputId = id || label?.toLowerCase().replace(/\s/g, "-");

  return (
    <div className="space-y-1.5">
      {label && (
        <label htmlFor={inputId} className="block text-sm font-medium text-brand-text">
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={`w-full rounded-lg border border-brand-border bg-brand-surface px-4 py-2.5 text-sm text-brand-text outline-none transition-colors placeholder:text-brand-text-muted focus:border-brand-secondary focus:ring-2 focus:ring-brand-secondary/20 ${error ? "border-brand-danger" : ""} ${className}`}
        {...props}
      />
      {error && <p className="text-sm text-brand-danger">{error}</p>}
    </div>
  );
}
