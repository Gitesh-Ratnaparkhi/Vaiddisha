// frontend/src/components/common/Button.tsx
import React from 'react';
import { Loader2 } from 'lucide-react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
    variant?: 'primary' | 'secondary' | 'danger' | 'outline';
    isLoading?: boolean;
    leftIcon?: React.ReactNode;
    rightIcon?: React.ReactNode;
}

export const Button: React.FC<ButtonProps> = ({
    children,
    variant = 'primary',
    isLoading = false,
    leftIcon,
    rightIcon,
    className = '',
    disabled,
    ...props
}) => {
    const baseStyles = "inline-flex items-center justify-center gap-2 px-4 py-2.5 rounded-xl font-medium text-sm transition-all focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed";

    const variants = {
        primary: "bg-teal-600 hover:bg-teal-700 text-white shadow-sm shadow-teal-600/20 focus:ring-teal-500",
        secondary: "bg-slate-800 hover:bg-slate-900 text-white focus:ring-slate-700",
        danger: "bg-rose-600 hover:bg-rose-700 text-white focus:ring-rose-500",
        outline: "border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 focus:ring-slate-300",
    };

    return (
        <button
            className={`${baseStyles} ${variants[variant]} ${className}`}
            disabled={disabled || isLoading}
            {...props}
        >
            {isLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : leftIcon}
            {children}
            {!isLoading && rightIcon}
        </button>
    );
};