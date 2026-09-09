// frontend/src/components/common/Input.tsx
import React from 'react';

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
    label?: string;
    error?: string;
    leftIcon?: React.ReactNode;
}

export const Input: React.FC<InputProps> = ({
    label,
    error,
    leftIcon,
    className = '',
    ...props
}) => {
    return (
        <div className="space-y-1.5 w-full">
            {label && <label className="block text-xs font-semibold text-slate-700">{label}</label>}
            <div className="relative rounded-xl shadow-sm">
                {leftIcon && (
                    <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none text-slate-400">
                        {leftIcon}
                    </div>
                )}
                <input
                    className={`w-full text-sm rounded-xl border border-slate-200 bg-white p-2.5 focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 focus:outline-none transition ${leftIcon ? 'pl-9' : ''
                        } ${error ? 'border-rose-400 focus:border-rose-500 focus:ring-rose-500/20' : ''} ${className}`}
                    {...props}
                />
            </div>
            {error && <p className="text-xs text-rose-600 font-medium">{error}</p>}
        </div>
    );
};