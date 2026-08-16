// frontend/src/components/common/AuthModal.tsx
import React, { useState } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { useToast } from '../../context/ToastContext';
import { Button } from './Button';
import { TermsModal } from './TermsModal';
import {
    X,
    Mail,
    Lock,
    User,
    MapPin,
    Stethoscope,
    Building,
    Award,
    IndianRupee
} from 'lucide-react';

interface AuthModalProps {
    onClose: () => void;
    onLoginSuccess?: () => void;
}

export const AuthModal: React.FC<AuthModalProps> = ({ onClose, onLoginSuccess }) => {
    const { login, register } = useAuth();
    const { showToast } = useToast();

    const [mode, setMode] = useState<'signin' | 'register'>('signin');
    const [role, setRole] = useState<'patient' | 'doctor'>('patient');
    const [loading, setLoading] = useState(false);
    const [agreedToTerms, setAgreedToTerms] = useState(false);
    const [showTermsModal, setShowTermsModal] = useState(false);

    // General Form Fields
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [name, setName] = useState('');
    const [city, setCity] = useState('');

    // Doctor-Specific Fields
    const [speciality, setSpeciality] = useState('General Physician');
    const [qualification, setQualification] = useState('');
    const [hospital, setHospital] = useState('');
    const [fee, setFee] = useState('₹500');

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();

        if (mode === 'register' && !agreedToTerms) {
            showToast('Please accept the Terms & Conditions to complete registration.', 'error');
            return;
        }

        setLoading(true);

        try {
            if (mode === 'signin') {
                await login({ email, password });
                showToast('Signed in successfully!', 'success');
            } else {
                const payload: any = {
                    email,
                    password,
                    name,
                    city,
                    role
                };

                if (role === 'doctor') {
                    payload.speciality = speciality;
                    payload.qualification = qualification;
                    payload.hospital = hospital;
                    payload.fee = fee;
                }

                await register(payload);
                showToast('Account registered successfully! Welcome to Vaiddisha AI.', 'success');
            }

            if (onLoginSuccess) onLoginSuccess();
            onClose();
        } catch (err: any) {
            showToast(err.message || 'Authentication failed. Please check your credentials.', 'error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4 animate-fade-in">
                <div className="bg-white w-full max-w-md rounded-2xl shadow-2xl border border-slate-100 p-6 relative max-h-[90vh] overflow-y-auto">

                    {/* Close Button */}
                    <button
                        onClick={onClose}
                        className="absolute top-4 right-4 p-1.5 text-slate-400 hover:text-slate-600 rounded-lg transition cursor-pointer"
                    >
                        <X className="w-5 h-5" />
                    </button>

                    {/* Modal Header */}
                    <div className="mb-5">
                        <h2 className="text-xl font-bold text-slate-900">
                            {mode === 'signin' ? 'Patient & Doctor Portal' : `${role === 'doctor' ? 'Doctor' : 'Patient'} Registration`}
                        </h2>
                        <p className="text-xs text-slate-500 mt-0.5">
                            {mode === 'signin'
                                ? 'Sign in to access your consultations and appointments.'
                                : 'Create an account to access clinical triage and bookings.'}
                        </p>
                    </div>

                    {/* Role Switcher (Visible in Register Mode) */}
                    {mode === 'register' && (
                        <div className="grid grid-cols-2 gap-2 bg-slate-100 p-1 rounded-xl mb-4 text-xs font-semibold">
                            <button
                                type="button"
                                onClick={() => setRole('patient')}
                                className={`py-2 rounded-lg flex items-center justify-center gap-1.5 transition cursor-pointer ${role === 'patient'
                                    ? 'bg-white text-teal-800 shadow-xs'
                                    : 'text-slate-600 hover:text-slate-900'
                                    }`}
                            >
                                <User className="w-3.5 h-3.5" />
                                I am a Patient
                            </button>
                            <button
                                type="button"
                                onClick={() => setRole('doctor')}
                                className={`py-2 rounded-lg flex items-center justify-center gap-1.5 transition cursor-pointer ${role === 'doctor'
                                    ? 'bg-white text-teal-800 shadow-xs'
                                    : 'text-slate-600 hover:text-slate-900'
                                    }`}
                            >
                                <Stethoscope className="w-3.5 h-3.5" />
                                I am a Doctor
                            </button>
                        </div>
                    )}

                    {/* Main Form */}
                    <form onSubmit={handleSubmit} className="space-y-3.5">
                        {mode === 'register' && (
                            <>
                                <div>
                                    <label className="block text-xs font-bold text-slate-700 mb-1">Full Name</label>
                                    <div className="relative">
                                        <User className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                                        <input
                                            type="text"
                                            required
                                            placeholder={role === 'doctor' ? 'Dr. Priya Sharma' : 'Amit Sharma'}
                                            value={name}
                                            onChange={(e) => setName(e.target.value)}
                                            className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-xs font-bold text-slate-700 mb-1">City</label>
                                    <div className="relative">
                                        <MapPin className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                                        <input
                                            type="text"
                                            required
                                            placeholder="Nagpur"
                                            value={city}
                                            onChange={(e) => setCity(e.target.value)}
                                            className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                        />
                                    </div>
                                </div>

                                {/* Doctor-Specific Form Fields */}
                                {role === 'doctor' && (
                                    <>
                                        <div>
                                            <label className="block text-xs font-bold text-slate-700 mb-1">Speciality</label>
                                            <div className="relative">
                                                <Stethoscope className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                                                <input
                                                    type="text"
                                                    required
                                                    placeholder="e.g. Cardiologist, Dermatologist, General Physician"
                                                    value={speciality}
                                                    onChange={(e) => setSpeciality(e.target.value)}
                                                    className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                                />
                                            </div>
                                        </div>

                                        <div className="grid grid-cols-2 gap-2">
                                            <div>
                                                <label className="block text-xs font-bold text-slate-700 mb-1">Qualification</label>
                                                <div className="relative">
                                                    <Award className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                                                    <input
                                                        type="text"
                                                        required
                                                        placeholder="MBBS, MD"
                                                        value={qualification}
                                                        onChange={(e) => setQualification(e.target.value)}
                                                        className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                                    />
                                                </div>
                                            </div>

                                            <div>
                                                <label className="block text-xs font-bold text-slate-700 mb-1">Consultation Fee</label>
                                                <div className="relative">
                                                    <IndianRupee className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                                                    <input
                                                        type="text"
                                                        required
                                                        placeholder="₹500"
                                                        value={fee}
                                                        onChange={(e) => setFee(e.target.value)}
                                                        className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                                    />
                                                </div>
                                            </div>
                                        </div>

                                        <div>
                                            <label className="block text-xs font-bold text-slate-700 mb-1">Hospital / Clinic Name</label>
                                            <div className="relative">
                                                <Building className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                                                <input
                                                    type="text"
                                                    required
                                                    placeholder="City Care Clinic, Civil Hospital"
                                                    value={hospital}
                                                    onChange={(e) => setHospital(e.target.value)}
                                                    className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                                />
                                            </div>
                                        </div>
                                    </>
                                )}
                            </>
                        )}

                        <div>
                            <label className="block text-xs font-bold text-slate-700 mb-1">Email Address</label>
                            <div className="relative">
                                <Mail className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                                <input
                                    type="email"
                                    required
                                    placeholder={role === 'doctor' && mode === 'register' ? 'doctor@hospital.com' : 'patient@example.com'}
                                    value={email}
                                    onChange={(e) => setEmail(e.target.value)}
                                    className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>
                        </div>

                        <div>
                            <label className="block text-xs font-bold text-slate-700 mb-1">Password</label>
                            <div className="relative">
                                <Lock className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
                                <input
                                    type="password"
                                    required
                                    placeholder="••••••••"
                                    value={password}
                                    onChange={(e) => setPassword(e.target.value)}
                                    className="w-full pl-9 pr-3 py-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                />
                            </div>
                        </div>

                        {/* Terms and Conditions Checkbox (Visible in Registration Mode) */}
                        {mode === 'register' && (
                            <div className="flex items-start gap-2 pt-1">
                                <input
                                    id="agree-terms"
                                    type="checkbox"
                                    checked={agreedToTerms}
                                    onChange={(e) => setAgreedToTerms(e.target.checked)}
                                    className="w-4 h-4 mt-0.5 rounded border-slate-300 text-teal-600 focus:ring-teal-500 cursor-pointer"
                                />
                                <label htmlFor="agree-terms" className="text-[11px] text-slate-600 leading-tight">
                                    I agree to the{' '}
                                    <button
                                        type="button"
                                        onClick={() => setShowTermsModal(true)}
                                        className="text-teal-600 font-bold underline hover:text-teal-800 cursor-pointer"
                                    >
                                        Terms & Conditions
                                    </button>{' '}
                                    and clinical decision support disclaimer.
                                </label>
                            </div>
                        )}

                        <Button
                            type="submit"
                            isLoading={loading}
                            className="w-full py-3 bg-teal-600 hover:bg-teal-700 text-white font-semibold rounded-xl transition shadow-sm mt-2"
                            variant="primary"
                        >
                            {mode === 'signin' ? 'Sign In' : `Register as ${role === 'doctor' ? 'Doctor' : 'Patient'}`}
                        </Button>
                    </form>

                    {/* Toggle between Sign In & Register */}
                    <div className="mt-4 text-center">
                        {mode === 'signin' ? (
                            <div className="space-y-1">
                                <button
                                    type="button"
                                    onClick={() => {
                                        setMode('register');
                                        setRole('patient');
                                    }}
                                    className="text-xs text-teal-700 hover:underline block w-full font-medium cursor-pointer"
                                >
                                    New patient? Create an account
                                </button>
                                <button
                                    type="button"
                                    onClick={() => {
                                        setMode('register');
                                        setRole('doctor');
                                    }}
                                    className="text-xs text-slate-500 hover:text-teal-700 hover:underline block w-full font-medium cursor-pointer"
                                >
                                    Are you a medical doctor? Register here
                                </button>
                            </div>
                        ) : (
                            <button
                                type="button"
                                onClick={() => setMode('signin')}
                                className="text-xs text-teal-700 hover:underline font-medium cursor-pointer"
                            >
                                Already registered? Sign In
                            </button>
                        )}
                    </div>

                </div>
            </div>

            {/* Terms & Conditions Modal Dialog */}
            <TermsModal
                isOpen={showTermsModal}
                onClose={() => setShowTermsModal(false)}
            />
        </>
    );
};

export default AuthModal;