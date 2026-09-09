// frontend/src/pages/DoctorDirectory.tsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../context/ToastContext';
import { API_BASE_URL, appointmentApi } from '../api';
import {
    Stethoscope,
    MapPin,
    Search,
    Building,
    Award,
    IndianRupee,
    Filter
} from 'lucide-react';
import { Button } from '../components/common/Button';

export const DoctorDirectory: React.FC = () => {
    const { user } = useAuth();
    const { showToast } = useToast();

    const [doctors, setDoctors] = useState<any[]>([]);
    const [loading, setLoading] = useState(false);

    // Search parameters
    const [speciality, setSpeciality] = useState('General Physician');
    const [location, setLocation] = useState('');
    const [showAdvanced, setShowAdvanced] = useState(false);
    const [country, setCountry] = useState('');
    const [state, setState] = useState('');
    const [city, setCity] = useState('Nagpur');
    const [postalCode, setPostalCode] = useState('');

    // Booking Modal State
    const [selectedDoctor, setSelectedDoctor] = useState<any | null>(null);
    const [bookingDate, setBookingDate] = useState('');
    const [bookingSlot, setBookingSlot] = useState('10:00 AM - 10:30 AM');
    const [bookingReason, setBookingReason] = useState('');
    const [isBooking, setIsBooking] = useState(false);

    const fetchDoctors = async () => {
        setLoading(true);
        try {
            const params = new URLSearchParams();
            if (speciality.trim()) params.append('speciality', speciality.trim());
            if (location.trim()) params.append('location', location.trim());
            if (country.trim()) params.append('country', country.trim());
            if (state.trim()) params.append('state', state.trim());
            if (city.trim()) params.append('city', city.trim());
            if (postalCode.trim()) params.append('postal_code', postalCode.trim());

            const res = await fetch(`${API_BASE_URL}/doctors/search?${params.toString()}`);
            const data = await res.json();
            if (data.status === 'success') {
                setDoctors(data.doctors || []);
            } else {
                setDoctors([]);
            }
        } catch (err) {
            showToast('Failed to fetch specialists.', 'error');
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchDoctors();
    }, []);

    const handleSearchSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        fetchDoctors();
    };

    const handleBookAppointment = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!user) {
            showToast('Please sign in to schedule a consultation.', 'error');
            return;
        }
        if (!bookingDate) {
            showToast('Please select an appointment date.', 'error');
            return;
        }

        const doctorName = selectedDoctor.name.startsWith('Dr.') ? selectedDoctor.name : `Dr. ${selectedDoctor.name}`;
        const doctorInfoStr = `${doctorName} (${selectedDoctor.speciality} - ${selectedDoctor.hospital || ''}) | ${selectedDoctor.email}`;

        setIsBooking(true);
        try {
            await appointmentApi.book({
                patient_email: user.email,
                doctor_info_str: doctorInfoStr,
                date: bookingDate,
                slot: bookingSlot,
                reason: bookingReason || 'General Consultation'
            });
            showToast(`Appointment booked successfully with ${selectedDoctor.name}!`, 'success');
            setSelectedDoctor(null);
            setBookingReason('');
            setBookingDate('');
        } catch (err: any) {
            showToast(err.message || 'Failed to book appointment.', 'error');
        } finally {
            setIsBooking(false);
        }
    };

    return (
        <div className="space-y-6 max-w-6xl mx-auto">

            {/* Search Filter Header Card */}
            <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                <form onSubmit={handleSearchSubmit} className="flex flex-col md:flex-row gap-3 items-center">

                    {/* Speciality Input */}
                    <div className="relative flex-1 w-full">
                        <Stethoscope className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                        <input
                            type="text"
                            placeholder="Speciality (e.g. General Physician, Cardiologist)"
                            value={speciality}
                            onChange={(e) => setSpeciality(e.target.value)}
                            className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                        />
                    </div>

                    {/* Quick Location Input */}
                    <div className="relative flex-1 w-full">
                        <MapPin className="w-4 h-4 text-slate-400 absolute left-3.5 top-3.5" />
                        <input
                            type="text"
                            placeholder="City, State, Country or Pincode"
                            value={location}
                            onChange={(e) => setLocation(e.target.value)}
                            className="w-full pl-10 pr-4 py-2.5 bg-slate-50 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                        />
                    </div>

                    <div className="flex gap-2 w-full md:w-auto">
                        <Button
                            type="button"
                            variant="outline"
                            onClick={() => setShowAdvanced(!showAdvanced)}
                            className="px-3 py-2.5 text-xs font-semibold"
                        >
                            <Filter className="w-4 h-4 mr-1 text-slate-500" />
                            {showAdvanced ? 'Simple' : 'Filters'}
                        </Button>

                        <Button
                            type="submit"
                            isLoading={loading}
                            className="px-6 py-2.5 bg-teal-600 hover:bg-teal-700 text-white rounded-xl text-sm font-semibold flex-1 md:flex-none"
                        >
                            <Search className="w-4 h-4 mr-1.5" /> Search
                        </Button>
                    </div>
                </form>

                {/* Hierarchical Location Breakdown (Country -> State -> City -> Postal Code) */}
                {showAdvanced && (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-3 pt-3 border-t border-slate-100">
                        <div>
                            <label className="block text-[11px] font-bold text-slate-600 mb-1">Country</label>
                            <input
                                type="text"
                                placeholder="India"
                                value={country}
                                onChange={(e) => setCountry(e.target.value)}
                                className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                            />
                        </div>
                        <div>
                            <label className="block text-[11px] font-bold text-slate-600 mb-1">State</label>
                            <input
                                type="text"
                                placeholder="Maharashtra"
                                value={state}
                                onChange={(e) => setState(e.target.value)}
                                className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                            />
                        </div>
                        <div>
                            <label className="block text-[11px] font-bold text-slate-600 mb-1">City</label>
                            <input
                                type="text"
                                placeholder="Nagpur"
                                value={city}
                                onChange={(e) => setCity(e.target.value)}
                                className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                            />
                        </div>
                        <div>
                            <label className="block text-[11px] font-bold text-slate-600 mb-1">Postal Code / Pincode</label>
                            <input
                                type="text"
                                placeholder="440001"
                                value={postalCode}
                                onChange={(e) => setPostalCode(e.target.value)}
                                className="w-full p-2 bg-slate-50 border border-slate-200 rounded-lg text-xs"
                            />
                        </div>
                    </div>
                )}
            </div>

            {/* Results Grid */}
            {loading ? (
                <div className="text-center py-16 text-slate-400 text-sm">Searching for verified specialists...</div>
            ) : doctors.length === 0 ? (
                <div className="bg-white p-12 text-center rounded-2xl border border-slate-200">
                    <Stethoscope className="w-12 h-12 text-slate-300 mx-auto mb-3" />
                    <h4 className="font-bold text-slate-800 text-sm">No specialists found matching your search criteria.</h4>
                    <p className="text-xs text-slate-400 mt-1">Try clearing your filters or searching by a broader city.</p>
                </div>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
                    {doctors.map((doc) => (
                        <div
                            key={doc.id}
                            className="bg-white rounded-2xl border border-slate-200/80 p-5 shadow-xs flex flex-col justify-between card-hover-effect"
                        >
                            <div className="space-y-3.5">
                                <div className="flex items-start justify-between">
                                    <div className="flex items-center gap-3">
                                        <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-teal-50 to-teal-100 text-teal-700 font-bold flex items-center justify-center text-lg border border-teal-200/60 shadow-xs">
                                            {doc.name[0]?.toUpperCase() || 'D'}
                                        </div>
                                        <div>
                                            <h4 className="font-bold text-slate-900 text-sm group-hover:text-teal-700 transition-colors">{doc.name}</h4>
                                            <p className="text-xs font-semibold text-teal-600">{doc.speciality}</p>
                                        </div>
                                    </div>
                                    <span className="text-xs font-bold text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-lg border border-emerald-200 flex items-center gap-1 shadow-xs">
                                        ★ {doc.rating}
                                    </span>
                                </div>

                                <div className="space-y-2 text-xs text-slate-600 pt-2 border-t border-slate-100">
                                    <div className="flex items-center gap-2">
                                        <Award className="w-3.5 h-3.5 text-teal-600" />
                                        <span>{doc.qualification} • {doc.experience}</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <Building className="w-3.5 h-3.5 text-teal-600" />
                                        <span className="truncate">{doc.hospital}</span>
                                    </div>
                                    <div className="flex items-center gap-2">
                                        <MapPin className="w-3.5 h-3.5 text-teal-600" />
                                        <span>{doc.city}{doc.state ? `, ${doc.state}` : ''}{doc.postal_code ? ` - ${doc.postal_code}` : ''}</span>
                                    </div>
                                    <div className="flex items-center gap-2 font-bold text-slate-800">
                                        <IndianRupee className="w-3.5 h-3.5 text-teal-600" />
                                        <span>Fee: {doc.fee}</span>
                                    </div>
                                </div>

                                {doc.description && (
                                    <p className="text-xs text-slate-500 line-clamp-2 pt-1">
                                        {doc.description}
                                    </p>
                                )}
                            </div>

                            <div className="pt-4 mt-4 border-t border-slate-100">
                                <Button
                                    onClick={() => setSelectedDoctor(doc)}
                                    className="w-full"
                                    variant="primary"
                                >
                                    Book Consultation
                                </Button>
                            </div>
                        </div>
                    ))}
                </div>
            )}

            {/* Booking Dialog Modal */}
            {selectedDoctor && (
                <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/40 backdrop-blur-xs p-4">
                    <div className="bg-white max-w-md w-full rounded-2xl p-6 shadow-xl border border-slate-100 space-y-4">
                        <h3 className="text-base font-bold text-slate-900 border-b pb-2">
                            Book Appointment with {selectedDoctor.name}
                        </h3>

                        <form onSubmit={handleBookAppointment} className="space-y-3.5">
                            <div>
                                <label className="block text-xs font-bold text-slate-700 mb-1">Select Date</label>
                                <input
                                    type="date"
                                    required
                                    min={new Date().toISOString().split('T')[0]}
                                    value={bookingDate}
                                    onChange={(e) => setBookingDate(e.target.value)}
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-bold text-slate-700 mb-1">Select Time Slot</label>
                                <select
                                    value={bookingSlot}
                                    onChange={(e) => setBookingSlot(e.target.value)}
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                >
                                    <option value="09:00 AM - 09:30 AM">09:00 AM - 09:30 AM</option>
                                    <option value="10:00 AM - 10:30 AM">10:00 AM - 10:30 AM</option>
                                    <option value="11:30 AM - 12:00 PM">11:30 AM - 12:00 PM</option>
                                    <option value="02:00 PM - 02:30 PM">02:00 PM - 02:30 PM</option>
                                    <option value="04:00 PM - 04:30 PM">04:00 PM - 04:30 PM</option>
                                    <option value="06:00 PM - 06:30 PM">06:00 PM - 06:30 PM</option>
                                </select>
                            </div>

                            <div>
                                <label className="block text-xs font-bold text-slate-700 mb-1">Reason for Consultation</label>
                                <textarea
                                    rows={3}
                                    placeholder="Describe your health concern or symptoms..."
                                    value={bookingReason}
                                    onChange={(e) => setBookingReason(e.target.value)}
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>

                            <div className="flex justify-end gap-2 pt-3 border-t">
                                <Button
                                    type="button"
                                    variant="outline"
                                    onClick={() => setSelectedDoctor(null)}
                                    disabled={isBooking}
                                >
                                    Cancel
                                </Button>
                                <Button
                                    type="submit"
                                    isLoading={isBooking}
                                    className="bg-teal-600 hover:bg-teal-700 text-white"
                                >
                                    Confirm Booking
                                </Button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

        </div>
    );
};

export default DoctorDirectory;