// frontend/src/pages/Appointments.tsx
import { useState, useEffect } from 'react';
import { appointmentApi } from '../api';
import type { Appointment } from '../types';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../context/ToastContext';
import { Calendar, CheckCircle2, XCircle, Clock, Check, Ban, Plus, RefreshCw } from 'lucide-react';

interface AppointmentsProps {
    onNavigateToDirectory?: () => void;
}

export default function Appointments({ onNavigateToDirectory }: AppointmentsProps) {
    const { user } = useAuth();
    const { showToast } = useToast();
    const [appointments, setAppointments] = useState<Appointment[]>([]);
    const [loading, setLoading] = useState(false);

    const isDoctor = user?.role?.toLowerCase() === 'doctor';

    const fetchAppointments = async () => {
        if (!user) return;
        setLoading(true);
        try {
            let res;
            if (isDoctor) {
                res = await appointmentApi.getDoctorAppointments(user.email);
            } else {
                res = await appointmentApi.getPatientAppointments(user.email);
            }
            setAppointments(res.appointments || []);
        } catch (err: any) {
            showToast(err.message || 'Failed to fetch appointments', 'error');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchAppointments();
    }, [user]);

    const handleStatusUpdate = async (id: number, newStatus: 'Confirmed' | 'Rejected' | 'Completed') => {
        if (!user) return;
        try {
            await appointmentApi.updateStatus({
                appointment_id: id,
                new_status: newStatus,
                doctor_email: user.email,
            });
            showToast(`Appointment status updated to ${newStatus}`, 'success');
            fetchAppointments();
        } catch (err: any) {
            showToast(err.message || 'Update failed', 'error');
        }
    };

    if (!user) {
        return (
            <div className="bg-white p-10 text-center rounded-2xl border border-slate-200">
                <Calendar className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                <h3 className="text-base font-bold text-slate-800">Authentication Required</h3>
                <p className="text-xs text-slate-500 mt-1">Please sign in to view your scheduled clinical appointments.</p>
            </div>
        );
    }

    const getStatusBadge = (status: string) => {
        switch (status) {
            case 'Confirmed':
                return <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200"><CheckCircle2 className="w-3 h-3" /> Confirmed</span>;
            case 'Rejected':
                return <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-rose-50 text-rose-700 border border-rose-200"><XCircle className="w-3 h-3" /> Rejected</span>;
            default:
                return <span className="inline-flex items-center gap-1 text-xs font-semibold px-2.5 py-0.5 rounded-full bg-amber-50 text-amber-700 border border-amber-200"><Clock className="w-3 h-3" /> Pending</span>;
        }
    };

    return (
        <div className="space-y-5">
            {/* Header with Quick Action Buttons */}
            <div className="flex justify-between items-center mb-6">
                <div>
                    <h2 className="text-xl font-bold text-slate-900">
                        {isDoctor ? 'Doctor Appointment Schedule' : 'My Clinical Bookings'}
                    </h2>
                    <p className="text-xs text-slate-500">Track and manage upcoming consultations.</p>
                </div>

                <div className="flex items-center gap-2">
                    {!isDoctor && onNavigateToDirectory && (
                        <button
                            type="button"
                            onClick={onNavigateToDirectory}
                            className="flex items-center gap-1.5 px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white rounded-xl text-xs font-semibold shadow-xs transition"
                        >
                            <Plus className="w-3.5 h-3.5" />
                            Book New Consultation
                        </button>
                    )}
                    <button
                        type="button"
                        onClick={fetchAppointments}
                        disabled={loading}
                        className="flex items-center gap-1.5 px-4 py-2 border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-xl text-xs font-semibold transition"
                    >
                        <RefreshCw className={`w-3.5 h-3.5 ${loading ? 'animate-spin' : ''}`} />
                        Refresh
                    </button>
                </div>
            </div>

            {/* Table */}
            <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
                <div className="overflow-x-auto">
                    <table className="w-full text-left text-xs text-slate-600">
                        <thead className="bg-slate-50 text-slate-700 uppercase font-semibold border-b border-slate-200 text-[11px]">
                            <tr>
                                <th className="p-4">ID</th>
                                <th className="p-4">{isDoctor ? 'Patient' : 'Doctor'}</th>
                                <th className="p-4">Date & Slot</th>
                                <th className="p-4">Reason</th>
                                <th className="p-4">Status</th>
                                {isDoctor && <th className="p-4 text-right">Actions</th>}
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                            {appointments.map((appt) => (
                                <tr key={appt.id} className="hover:bg-slate-50/50 transition">
                                    <td className="p-4 font-mono font-medium text-slate-500">#{appt.id}</td>
                                    <td className="p-4 font-semibold text-slate-800">
                                        {isDoctor ? appt.patient_email : (appt.doctor_name || appt.doctor_email)}
                                    </td>
                                    <td className="p-4">
                                        <span className="font-medium text-slate-700">{appt.date}</span>
                                        <span className="block text-[11px] text-slate-400">{appt.slot}</span>
                                    </td>
                                    <td className="p-4 max-w-xs truncate text-slate-500">{appt.reason || 'General checkup'}</td>
                                    <td className="p-4">{getStatusBadge(appt.status)}</td>
                                    {isDoctor && (
                                        <td className="p-4 text-right space-x-1.5">
                                            {appt.status === 'Pending' && (
                                                <>
                                                    <button
                                                        onClick={() => handleStatusUpdate(appt.id, 'Confirmed')}
                                                        className="p-1.5 bg-emerald-50 hover:bg-emerald-100 text-emerald-700 rounded-lg transition"
                                                        title="Confirm"
                                                    >
                                                        <Check className="w-4 h-4" />
                                                    </button>
                                                    <button
                                                        onClick={() => handleStatusUpdate(appt.id, 'Rejected')}
                                                        className="p-1.5 bg-rose-50 hover:bg-rose-100 text-rose-700 rounded-lg transition"
                                                        title="Reject"
                                                    >
                                                        <Ban className="w-4 h-4" />
                                                    </button>
                                                </>
                                            )}
                                        </td>
                                    )}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {appointments.length === 0 && !loading && (
                    <div className="text-center py-10 text-slate-400 text-xs">
                        No scheduled appointments found.
                    </div>
                )}
            </div>
        </div>
    );
}