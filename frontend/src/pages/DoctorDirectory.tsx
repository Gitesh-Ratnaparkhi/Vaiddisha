// frontend/src/pages/DoctorDirectory.tsx
import React, { useState, useEffect } from 'react';
import { doctorApi, appointmentApi } from '../api';
import type { DoctorProfile } from '../types';
import { DoctorCard } from '../components/medical/DoctorCard';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../context/ToastContext';
import { Search, MapPin, Stethoscope, Calendar, Clock, X } from 'lucide-react';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';

export default function DoctorDirectory() {
    const { user } = useAuth();
    const { showToast } = useToast();

    const [doctors, setDoctors] = useState<DoctorProfile[]>([]);
    const [specialityFilter, setSpecialityFilter] = useState('');
    const [cityFilter, setCityFilter] = useState('');
    const [loading, setLoading] = useState(false);

    // Booking Modal State
    const [selectedDoctor, setSelectedDoctor] = useState<DoctorProfile | null>(null);
    const [bookingDate, setBookingDate] = useState('');
    const [bookingSlot, setBookingSlot] = useState('10:00 AM - 10:30 AM');
    const [bookingReason, setBookingReason] = useState('');
    const [submittingBooking, setSubmittingBooking] = useState(false);

    const fetchDoctors = async () => {
        setLoading(true);
        try {
            const res = await doctorApi.searchDoctors({
                speciality: specialityFilter || undefined,
                city: cityFilter || undefined,
            });
            setDoctors(res.doctors || []);
        } catch (err: any) {
            showToast(err.message || 'Failed to load doctors list', 'error');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDoctors();
    }, []);

    const handleBookAppointment = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!user) {
            showToast('Please sign in to schedule an appointment.', 'error');
            return;
        }
        if (!selectedDoctor) return;

        setSubmittingBooking(true);
        try {
            const doctorInfoStr = `${selectedDoctor.name} | ${selectedDoctor.speciality} | ${selectedDoctor.city} | ${selectedDoctor.email}`;
            await appointmentApi.book({
                patient_email: user.email,
                doctor_info_str: doctorInfoStr,
                date: bookingDate,
                slot: bookingSlot,
                reason: bookingReason,
            });
            showToast('Appointment booked successfully! Awaiting confirmation.', 'success');
            setSelectedDoctor(null);
            setBookingReason('');
        } catch (err: any) {
            showToast(err.message || 'Failed to book appointment', 'error');
        } finally {
            setSubmittingBooking(false);
        }
    };

    return (
        <div className="space-y-6">
            {/* Search Header */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col md:flex-row gap-3 items-center">
                <div className="flex-1 w-full relative">
                    <Stethoscope className="w-4 h-4 absolute left-3 top-3.5 text-slate-400" />
                    <input
                        type="text"
                        placeholder="Search by Speciality (e.g. Cardiologist, Dermatologist)..."
                        value={specialityFilter}
                        onChange={(e) => setSpecialityFilter(e.target.value)}
                        className="w-full pl-9 p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                    />
                </div>
                <div className="w-full md:w-64 relative">
                    <MapPin className="w-4 h-4 absolute left-3 top-3.5 text-slate-400" />
                    <input
                        type="text"
                        placeholder="City (e.g. Nagpur, Mumbai)..."
                        value={cityFilter}
                        onChange={(e) => setCityFilter(e.target.value)}
                        className="w-full pl-9 p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                    />
                </div>
                <Button
                    onClick={fetchDoctors}
                    isLoading={loading}
                    className="w-full md:w-auto"
                    leftIcon={<Search className="w-4 h-4" />}
                >
                    Search
                </Button>
            </div>

            {/* Doctor Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                {doctors.map((doc) => (
                    <DoctorCard
                        key={doc.email}
                        doctor={doc}
                        onBookClick={(d) => setSelectedDoctor(d)}
                    />
                ))}
            </div>

            {doctors.length === 0 && !loading && (
                <div className="text-center py-12 bg-white rounded-2xl border border-slate-200">
                    <Stethoscope className="w-10 h-10 mx-auto text-slate-300 mb-2" />
                    <p className="text-slate-500 text-sm">No specialists found matching your search criteria.</p>
                </div>
            )}

            {/* Appointment Booking Modal */}
            {selectedDoctor && (
                <div className="fixed inset-0 z-50 bg-black/40 backdrop-blur-sm flex items-center justify-center p-4">
                    <div className="bg-white rounded-2xl max-w-md w-full p-6 shadow-xl border border-slate-100 relative">
                        <button
                            onClick={() => setSelectedDoctor(null)}
                            className="absolute right-4 top-4 text-slate-400 hover:text-slate-600"
                        >
                            <X className="w-5 h-5" />
                        </button>

                        <h3 className="text-lg font-bold text-slate-900 mb-1">Book Consultation</h3>
                        <p className="text-xs text-slate-500 mb-4">
                            Booking with <span className="font-semibold text-teal-700">{selectedDoctor.name}</span> ({selectedDoctor.speciality})
                        </p>

                        <form onSubmit={handleBookAppointment} className="space-y-3.5">
                            <Input
                                label="Appointment Date"
                                type="date"
                                required
                                value={bookingDate}
                                onChange={(e) => setBookingDate(e.target.value)}
                                leftIcon={<Calendar className="w-4 h-4" />}
                            />

                            <div className="space-y-1.5">
                                <label className="block text-xs font-semibold text-slate-700">Time Slot</label>
                                <div className="relative">
                                    <Clock className="w-4 h-4 absolute left-3 top-3 text-slate-400" />
                                    <select
                                        value={bookingSlot}
                                        onChange={(e) => setBookingSlot(e.target.value)}
                                        className="w-full pl-9 p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none bg-white"
                                    >
                                        <option value="09:00 AM - 09:30 AM">09:00 AM - 09:30 AM</option>
                                        <option value="10:00 AM - 10:30 AM">10:00 AM - 10:30 AM</option>
                                        <option value="11:30 AM - 12:00 PM">11:30 AM - 12:00 PM</option>
                                        <option value="02:00 PM - 02:30 PM">02:00 PM - 02:30 PM</option>
                                        <option value="04:00 PM - 04:30 PM">04:00 PM - 04:30 PM</option>
                                    </select>
                                </div>
                            </div>

                            <div className="space-y-1.5">
                                <label className="block text-xs font-semibold text-slate-700">Reason / Symptoms</label>
                                <textarea
                                    rows={2}
                                    value={bookingReason}
                                    onChange={(e) => setBookingReason(e.target.value)}
                                    placeholder="Primary reason for scheduling this visit..."
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>

                            <Button
                                type="submit"
                                isLoading={submittingBooking}
                                className="w-full mt-2"
                            >
                                Confirm Appointment
                            </Button>
                        </form>
                    </div>
                </div>
            )}
        </div>
    );
}