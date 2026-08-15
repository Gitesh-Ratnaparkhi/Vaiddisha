// frontend/src/components/medical/DoctorCard.tsx
import React from 'react';
import type { DoctorProfile } from '../../types';
import { Stethoscope, Building2, MapPin, Phone, CalendarCheck } from 'lucide-react';
import { Button } from '../common/Button';

interface DoctorCardProps {
    doctor: DoctorProfile;
    onBookClick: (doctor: DoctorProfile) => void;
}

export const DoctorCard: React.FC<DoctorCardProps> = ({ doctor, onBookClick }) => {
    return (
        <div className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-sm hover:shadow-md transition-all flex flex-col justify-between">
            <div>
                <div className="flex items-start justify-between gap-3 mb-3">
                    <div>
                        <h4 className="font-bold text-slate-900 text-base">{doctor.name}</h4>
                        <span className="inline-flex items-center gap-1 text-xs font-semibold text-teal-700 bg-teal-50 px-2.5 py-0.5 rounded-full mt-1">
                            <Stethoscope className="w-3 h-3" />
                            {doctor.speciality}
                        </span>
                    </div>
                    <span className="font-bold text-slate-800 text-sm bg-slate-100 px-2.5 py-1 rounded-lg border border-slate-200">
                        {doctor.fee}
                    </span>
                </div>

                <p className="text-xs text-slate-600 mb-3 line-clamp-2">{doctor.description || 'Specialist doctor.'}</p>

                <div className="space-y-1.5 text-xs text-slate-500 mb-4">
                    <div className="flex items-center gap-2">
                        <Building2 className="w-3.5 h-3.5 text-slate-400" />
                        <span>{doctor.hospital} ({doctor.experience} exp)</span>
                    </div>
                    <div className="flex items-center gap-2">
                        <MapPin className="w-3.5 h-3.5 text-slate-400" />
                        <span>{doctor.city}, {doctor.state}</span>
                    </div>
                    {doctor.phone && (
                        <div className="flex items-center gap-2">
                            <Phone className="w-3.5 h-3.5 text-slate-400" />
                            <span>{doctor.phone}</span>
                        </div>
                    )}
                </div>
            </div>

            <Button
                variant="primary"
                className="w-full text-xs py-2"
                leftIcon={<CalendarCheck className="w-4 h-4" />}
                onClick={() => onBookClick(doctor)}
            >
                Book Consultation
            </Button>
        </div>
    );
};