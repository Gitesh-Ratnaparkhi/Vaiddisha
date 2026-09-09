// frontend/src/components/medical/UrgencyBadge.tsx
import React from 'react';
import type { UrgencyLevel } from '../../types';
import { AlertCircle, AlertTriangle, CheckCircle, Flame } from 'lucide-react';

export const UrgencyBadge: React.FC<{ level: UrgencyLevel }> = ({ level }) => {
    const configs = {
        Low: {
            color: 'bg-emerald-50 text-emerald-700 border-emerald-200',
            icon: <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />,
            label: 'Low Urgency'
        },
        Moderate: {
            color: 'bg-amber-50 text-amber-700 border-amber-200',
            icon: <AlertTriangle className="w-3.5 h-3.5 text-amber-600" />,
            label: 'Moderate Urgency'
        },
        High: {
            color: 'bg-orange-50 text-orange-700 border-orange-200',
            icon: <AlertCircle className="w-3.5 h-3.5 text-orange-600" />,
            label: 'High Urgency'
        },
        Emergency: {
            color: 'bg-rose-50 text-rose-700 border-rose-300 animate-pulse',
            icon: <Flame className="w-3.5 h-3.5 text-rose-600" />,
            label: 'Emergency Attention Needed'
        },
    };

    const selected = configs[level] || configs.Low;

    return (
        <div className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full border text-xs font-semibold ${selected.color}`}>
            {selected.icon}
            <span>{selected.label}</span>
        </div>
    );
};