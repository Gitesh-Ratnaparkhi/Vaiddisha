// frontend/src/components/layout/Footer.tsx
import React from 'react';
import type { TabType } from './Navbar';
import {
    ShieldAlert,
    PhoneCall,
    Mail,
    MapPin,
    Stethoscope,
    Lock
} from 'lucide-react';

interface FooterProps {
    setActiveTab?: (tab: TabType) => void;
    isDoctor?: boolean;
    onOpenPrivacyPolicy?: () => void;
}

export const Footer: React.FC<FooterProps> = ({ setActiveTab, isDoctor, onOpenPrivacyPolicy }) => {
    return (
        <footer className="relative mt-auto">
            {/* Smooth Gradient Transition Divider (from light slate-50 to dark slate-900) */}
            <div className="h-20 bg-gradient-to-b from-slate-50 via-slate-200/50 to-slate-900 pointer-events-none" />

            {/* Main Footer Container */}
            <div className="bg-slate-900 text-slate-300 pt-4 pb-8">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">

                    {/* Top Grid */}
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8 pb-8 border-b border-slate-800">

                        {/* Brand Info */}
                        <div className="space-y-3">
                            <div className="flex items-center gap-2.5">
                                <div className="w-8 h-8 rounded-lg bg-teal-500 flex items-center justify-center text-white font-bold text-sm shadow-md">
                                    ⚕️
                                </div>
                                <span className="text-lg font-bold text-white tracking-tight">
                                    Vaiddisha <span className="text-teal-400">AI</span>
                                </span>
                            </div>
                            <p className="text-xs text-slate-400 leading-relaxed">
                                Clinical decision-support system delivering AI-assisted differential diagnosis, intelligent lab report vision OCR, and certified specialist booking.
                            </p>
                            <div className="flex items-center gap-2 text-xs text-teal-400 font-medium">
                                <Lock className="w-3.5 h-3.5" />
                                <span>HIPAA & GDPR Compliant Architecture</span>
                            </div>
                        </div>

                        {/* Quick Navigation */}
                        <div className="space-y-3">
                            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-100">
                                Clinical Services
                            </h4>
                            <ul className="space-y-2 text-xs">
                                {!isDoctor ? (
                                    <>
                                        <li>
                                            <button
                                                onClick={() => setActiveTab?.('triage')}
                                                className="hover:text-teal-400 transition flex items-center gap-1.5 cursor-pointer"
                                            >
                                                🩺 AI Symptom Triage
                                            </button>
                                        </li>
                                        <li>
                                            <button
                                                onClick={() => setActiveTab?.('lab')}
                                                className="hover:text-teal-400 transition flex items-center gap-1.5 cursor-pointer"
                                            >
                                                📋 Lab Vision OCR Analyzer
                                            </button>
                                        </li>
                                        <li>
                                            <button
                                                onClick={() => setActiveTab?.('doctors')}
                                                className="hover:text-teal-400 transition flex items-center gap-1.5 cursor-pointer"
                                            >
                                                👨‍⚕️ Specialist Directory
                                            </button>
                                        </li>
                                    </>
                                ) : null}
                                <li>
                                    <button
                                        onClick={() => setActiveTab?.('appointments')}
                                        className="hover:text-teal-400 transition flex items-center gap-1.5 cursor-pointer"
                                    >
                                        📅 Consultations & Bookings
                                    </button>
                                </li>
                                <li>
                                    <button
                                        onClick={() => setActiveTab?.('profile')}
                                        className="hover:text-teal-400 transition flex items-center gap-1.5 cursor-pointer"
                                    >
                                        👤 {isDoctor ? 'Doctor Clinical Profile' : 'Patient Health Profile'}
                                    </button>
                                </li>
                            </ul>
                        </div>

                        {/* Emergency Helpline */}
                        <div className="space-y-3">
                            <h4 className="text-xs font-bold uppercase tracking-wider text-rose-400 flex items-center gap-1.5">
                                <ShieldAlert className="w-4 h-4" /> Emergency Helplines
                            </h4>
                            <div className="space-y-2 text-xs text-slate-300">
                                <div className="p-2.5 rounded-xl bg-slate-800/80 border border-slate-700">
                                    <div className="text-[11px] text-slate-400 font-medium">National Emergency (India)</div>
                                    <div className="text-base font-bold text-white flex items-center gap-2 mt-0.5">
                                        <PhoneCall className="w-4 h-4 text-teal-400" /> 112 / 108
                                    </div>
                                </div>
                                <div className="p-2.5 rounded-xl bg-slate-800/80 border border-slate-700">
                                    <div className="text-[11px] text-slate-400 font-medium">Ambulance & Trauma Support</div>
                                    <div className="text-sm font-semibold text-rose-300">24/7 Immediate Dispatch</div>
                                </div>
                            </div>
                        </div>

                        {/* Contact & Location */}
                        <div className="space-y-3">
                            <h4 className="text-xs font-bold uppercase tracking-wider text-slate-100">
                                Contact & Support
                            </h4>
                            <div className="space-y-2 text-xs text-slate-400">
                                <div className="flex items-center gap-2">
                                    <MapPin className="w-3.5 h-3.5 text-teal-400 shrink-0" />
                                    <span>Nagpur, Maharashtra, India</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Mail className="w-3.5 h-3.5 text-teal-400 shrink-0" />
                                    <span>support@vaiddisha.ai</span>
                                </div>
                                <div className="flex items-center gap-2">
                                    <Stethoscope className="w-3.5 h-3.5 text-teal-400 shrink-0" />
                                    <span>Medical Panel & Verification Desk</span>
                                </div>
                            </div>
                        </div>

                    </div>

                    {/* Clinical Disclaimer */}
                    <div className="py-4 text-[11px] text-slate-500 leading-relaxed border-b border-slate-800">
                        <strong className="text-slate-400 font-semibold">Medical Disclaimer: </strong>
                        Vaiddisha AI is an artificial intelligence-assisted clinical decision support tool intended solely for informational, preliminary triage, and educational purposes. It does not provide definitive medical diagnoses, prescriptions, or replace formal consultation with qualified healthcare professionals. In any medical emergency, please call emergency services (112 / 108) or visit the nearest trauma care facility immediately.
                    </div>

                    {/* Bottom Bar */}
                    <div className="pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 gap-3">
                        <p>© {new Date().getFullYear()} Vaiddisha AI. All rights reserved.</p>
                        <div className="flex items-center gap-4">
                            <button
                                type="button"
                                onClick={onOpenPrivacyPolicy}
                                className="hover:text-teal-400 cursor-pointer underline transition"
                            >
                                Privacy Policy
                            </button>
                            <span>•</span>
                            <button
                                type="button"
                                onClick={onOpenPrivacyPolicy}
                                className="hover:text-teal-400 cursor-pointer transition"
                            >
                                Terms of Service
                            </button>
                            <span>•</span>
                            <span className="text-slate-600">Clinical Protocols</span>
                        </div>
                    </div>

                </div>
            </div>
        </footer>
    );
};

export default Footer;