// frontend/src/components/medical/SafetyBanner.tsx
import React from 'react';
import { ShieldAlert } from 'lucide-react';

export const SafetyBanner: React.FC<{ warnings: string[] }> = ({ warnings }) => {
    if (!warnings || warnings.length === 0) return null;

    return (
        <div className="bg-amber-50/80 border border-amber-200 rounded-xl p-4 my-3 text-amber-900 text-xs">
            <div className="flex items-center gap-2 font-bold mb-1 text-amber-800">
                <ShieldAlert className="w-4 h-4 text-amber-600" />
                Clinical Safety Alert & Precautions
            </div>
            <ul className="list-disc list-inside space-y-1 mt-1 text-amber-800/90">
                {warnings.map((w, idx) => (
                    <li key={idx}>{w}</li>
                ))}
            </ul>
        </div>
    );
};