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
        <label htmlFor={inputId} className="block text-sm font-medium text-slate-700">
          {label}
        </label>
      )}
      <input
        id={inputId}
        className={`w-full rounded-xl border border-brand-border bg-slate-50/50 px-4 py-3 text-sm text-slate-900 outline-none transition-all placeholder:text-slate-400 hover:border-brand-primary/40 focus:border-brand-primary focus:bg-white focus:ring-4 focus:ring-brand-primary/10 ${error ? "border-brand-danger focus:ring-brand-danger/10" : ""} ${className}`}
        {...props}
      />
      {error && <p className="text-sm text-brand-danger">{error}</p>}
    </div>
  );
}
