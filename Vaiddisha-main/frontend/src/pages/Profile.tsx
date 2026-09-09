// frontend/src/pages/Profile.tsx
import React, { useState, useEffect } from 'react';
import { useAuth } from '../hooks/useAuth';
import { useToast } from '../context/ToastContext';
import { API_BASE_URL } from '../api';
import { User, Stethoscope, Save, Activity, Award } from 'lucide-react';

export const Profile: React.FC = () => {
    const { user } = useAuth();
    const { showToast } = useToast();
    const [loading, setLoading] = useState(false);
    const [saving, setSaving] = useState(false);

    const isDoctor = user?.role?.toLowerCase() === 'doctor';

    // Form State
    const [formData, setFormData] = useState<any>({
        email: user?.email || '',
        name: user?.name || '',
        phone: '',
        city: '',
        state: '',
        country: 'India',
        postal_code: '',
        // Patient specific
        gender: 'Male',
        age: '',
        conditions: '',
        surgeries: '',
        allergies: '',
        // Doctor specific
        speciality: 'General Physician',
        qualification: '',
        experience: '',
        hospital: '',
        fee: '',
        description: ''
    });

    useEffect(() => {
        if (!user?.email) return;
        setLoading(true);
        fetch(`${API_BASE_URL}/profile/get?email=${encodeURIComponent(user.email)}&role=${user.role || 'patient'}`)
            .then(res => res.json())
            .then(data => {
                if (data.status === 'success' && data.profile) {
                    setFormData((prev: any) => ({ ...prev, ...data.profile }));
                }
            })
            .catch(() => showToast('Could not fetch existing profile', 'error'))
            .finally(() => setLoading(false));
    }, [user]);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
        setFormData({ ...formData, [e.target.name]: e.target.value });
    };

    const handleSave = async (e: React.FormEvent) => {
        e.preventDefault();
        setSaving(true);
        const endpoint = isDoctor ? '/profile/update/doctor' : '/profile/update/patient';

        try {
            const res = await fetch(`${API_BASE_URL}${endpoint}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            const data = await res.json();
            if (data.status === 'success') {
                showToast('Profile updated successfully!', 'success');
            } else {
                showToast(data.detail || 'Failed to update profile', 'error');
            }
        } catch (err) {
            showToast('Network error while saving profile', 'error');
        } finally {
            setSaving(false);
        }
    };

    if (loading) {
        return <div className="p-8 text-center text-slate-500">Loading profile...</div>;
    }

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Profile Header */}
            <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex items-center gap-4">
                <div className="w-16 h-16 rounded-2xl bg-teal-600 flex items-center justify-center text-white text-2xl font-bold">
                    {isDoctor ? <Stethoscope className="w-8 h-8" /> : <User className="w-8 h-8" />}
                </div>
                <div>
                    <h2 className="text-xl font-bold text-slate-900">{formData.name || 'User Profile'}</h2>
                    <p className="text-sm text-slate-500">{user?.email} • <span className="text-teal-600 font-semibold uppercase">{user?.role}</span></p>
                </div>
            </div>

            {/* Main Profile Form */}
            <form onSubmit={handleSave} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">

                <h3 className="text-md font-bold text-slate-800 border-b pb-2 flex items-center gap-2">
                    <User className="w-4 h-4 text-teal-600" /> Basic Details
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label className="block text-xs font-bold text-slate-700 mb-1">Full Name</label>
                        <input
                            name="name"
                            value={formData.name || ''}
                            onChange={handleChange}
                            required
                            className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                        />
                    </div>

                    <div>
                        <label className="block text-xs font-bold text-slate-700 mb-1">Phone Number</label>
                        <input
                            name="phone"
                            value={formData.phone || ''}
                            onChange={handleChange}
                            placeholder="+91 9876543210"
                            className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                        />
                    </div>

                    <div>
                        <label className="block text-xs font-bold text-slate-700 mb-1">City</label>
                        <input
                            name="city"
                            value={formData.city || ''}
                            onChange={handleChange}
                            placeholder="e.g. Mumbai, Nagpur"
                            className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                        />
                    </div>

                    <div>
                        <label className="block text-xs font-bold text-slate-700 mb-1">State</label>
                        <input
                            name="state"
                            value={formData.state || ''}
                            onChange={handleChange}
                            placeholder="e.g. Maharashtra"
                            className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                        />
                    </div>
                </div>

                {/* ROLE SPECIFIC FIELDS */}
                {isDoctor ? (
                    <>
                        <h3 className="text-md font-bold text-slate-800 border-b pb-2 pt-2 flex items-center gap-2">
                            <Award className="w-4 h-4 text-teal-600" /> Clinical & Practice Details
                        </h3>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-xs font-bold text-slate-700 mb-1">Speciality</label>
                                <input
                                    name="speciality"
                                    value={formData.speciality || ''}
                                    onChange={handleChange}
                                    required
                                    placeholder="e.g., Cardiologist, Dermatologist"
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-bold text-slate-700 mb-1">Qualification</label>
                                <input
                                    name="qualification"
                                    value={formData.qualification || ''}
                                    onChange={handleChange}
                                    placeholder="e.g., MBBS, MD, MS"
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-bold text-slate-700 mb-1">Hospital / Clinic Name</label>
                                <input
                                    name="hospital"
                                    value={formData.hospital || ''}
                                    onChange={handleChange}
                                    placeholder="e.g., City Care Hospital"
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-bold text-slate-700 mb-1">Consultation Fee (₹)</label>
                                <input
                                    name="fee"
                                    value={formData.fee || ''}
                                    onChange={handleChange}
                                    placeholder="e.g., ₹500"
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-xs font-bold text-slate-700 mb-1">About / Bio</label>
                            <textarea
                                name="description"
                                rows={3}
                                value={formData.description || ''}
                                onChange={handleChange}
                                placeholder="Brief summary of your medical experience and expertise..."
                                className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                            />
                        </div>
                    </>
                ) : (
                    <>
                        <h3 className="text-md font-bold text-slate-800 border-b pb-2 pt-2 flex items-center gap-2">
                            <Activity className="w-4 h-4 text-teal-600" /> Medical Background (For AI Triage Context)
                        </h3>

                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            <div>
                                <label className="block text-xs font-bold text-slate-700 mb-1">Age</label>
                                <input
                                    type="number"
                                    name="age"
                                    value={formData.age || ''}
                                    onChange={handleChange}
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-bold text-slate-700 mb-1">Gender</label>
                                <select
                                    name="gender"
                                    value={formData.gender || 'Male'}
                                    onChange={handleChange}
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                >
                                    <option value="Male">Male</option>
                                    <option value="Female">Female</option>
                                    <option value="Other">Other</option>
                                </select>
                            </div>
                        </div>

                        <div className="space-y-3">
                            <div>
                                <label className="block text-xs font-bold text-slate-700 mb-1">Existing Medical Conditions / History</label>
                                <input
                                    name="conditions"
                                    value={formData.conditions || ''}
                                    onChange={handleChange}
                                    placeholder="e.g., Hypertension, Diabetes Type 2, Asthma"
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>

                            <div>
                                <label className="block text-xs font-bold text-slate-700 mb-1">Known Drug or Food Allergies</label>
                                <input
                                    name="allergies"
                                    value={formData.allergies || ''}
                                    onChange={handleChange}
                                    placeholder="e.g., Penicillin, Peanuts, Sulfa drugs"
                                    className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>
                        </div>
                    </>
                )}

                <div className="flex justify-end pt-4 border-t border-slate-100">
                    <button
                        type="submit"
                        disabled={saving}
                        className="flex items-center gap-2 px-6 py-2.5 bg-teal-600 hover:bg-teal-700 text-white rounded-xl font-semibold text-sm shadow-sm transition"
                    >
                        <Save className="w-4 h-4" />
                        {saving ? 'Saving...' : 'Save Profile'}
                    </button>
                </div>
            </form>
        </div>
    );
};

export default Profile;