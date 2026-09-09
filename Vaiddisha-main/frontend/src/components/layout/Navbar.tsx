// frontend/src/components/layout/Navbar.tsx
import React, { useState, useRef, useEffect } from 'react';
import { useAuth } from '../../hooks/useAuth';
import { User, LogOut, ChevronDown, ShieldCheck, Stethoscope } from 'lucide-react';

export type TabType = 'triage' | 'lab' | 'doctors' | 'appointments' | 'profile';

interface NavbarProps {
    activeTab: TabType;
    setActiveTab: (tab: TabType) => void;
}

export const Navbar: React.FC<NavbarProps> = ({ activeTab, setActiveTab }) => {
    const { user, logout } = useAuth();
    const isDoctor = user?.role?.toLowerCase() === 'doctor';
    const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    // Close dropdown on clicking outside
    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setIsProfileMenuOpen(false);
            }
        };
        document.addEventListener('mousedown', handleClickOutside);
        return () => document.removeEventListener('mousedown', handleClickOutside);
    }, []);

    return (
        <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200/80 shadow-xs transition-colors duration-200">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between">

                {/* Left: Brand Logo & Title */}
                <div
                    className="flex items-center gap-3 cursor-pointer group select-none"
                    onClick={() => setActiveTab(isDoctor ? 'appointments' : 'triage')}
                >
                    <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-teal-700 to-teal-500 flex items-center justify-center text-white font-bold shadow-xs group-hover:scale-105 group-hover:shadow-teal-500/30 transition-transform duration-200">
                        ⚕️
                    </div>
                    <div>
                        <div className="text-xl font-bold text-slate-900 tracking-tight group-hover:text-teal-700 transition-colors">
                            Vaiddisha <span className="text-teal-600">AI</span>
                        </div>
                        <div className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
                            {isDoctor ? 'Doctor Portal' : 'Clinical Decision Support'}
                        </div>
                    </div>
                </div>

                {/* Center: Main Navigation Tabs */}
                <nav className="hidden md:flex items-center gap-1.5 bg-slate-100/90 p-1.5 rounded-2xl border border-slate-200/60">
                    {!isDoctor && (
                        <>
                            <button
                                onClick={() => setActiveTab('triage')}
                                className={`px-3.5 py-1.5 text-xs font-semibold rounded-xl cursor-pointer transition-all duration-200 ${activeTab === 'triage'
                                        ? 'bg-white text-teal-800 shadow-xs font-bold'
                                        : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                                    }`}
                            >
                                🩺 Symptom Triage
                            </button>
                            <button
                                onClick={() => setActiveTab('lab')}
                                className={`px-3.5 py-1.5 text-xs font-semibold rounded-xl cursor-pointer transition-all duration-200 ${activeTab === 'lab'
                                        ? 'bg-white text-teal-800 shadow-xs font-bold'
                                        : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                                    }`}
                            >
                                📋 Lab Vision OCR
                            </button>
                            <button
                                onClick={() => setActiveTab('doctors')}
                                className={`px-3.5 py-1.5 text-xs font-semibold rounded-xl cursor-pointer transition-all duration-200 ${activeTab === 'doctors'
                                        ? 'bg-white text-teal-800 shadow-xs font-bold'
                                        : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                                    }`}
                            >
                                👨‍⚕️ Specialists
                            </button>
                        </>
                    )}

                    <button
                        onClick={() => setActiveTab('appointments')}
                        className={`px-3.5 py-1.5 text-xs font-semibold rounded-xl cursor-pointer transition-all duration-200 ${activeTab === 'appointments'
                                ? 'bg-white text-teal-800 shadow-xs font-bold'
                                : 'text-slate-600 hover:text-slate-900 hover:bg-white/50'
                            }`}
                    >
                        📅 {isDoctor ? 'Consultations' : 'Appointments'}
                    </button>
                </nav>

                {/* Right: Translate & Profile Dropdown */}
                <div className="flex items-center gap-3">
                    <div id="google_translate_element" className="notranslate-icon text-xs"></div>

                    {/* Profile Dropdown Menu */}
                    <div className="relative" ref={dropdownRef}>
                        <button
                            onClick={() => setIsProfileMenuOpen(!isProfileMenuOpen)}
                            className={`flex items-center gap-2 pl-2 pr-3 py-1.5 rounded-xl border transition-all duration-200 cursor-pointer ${activeTab === 'profile' || isProfileMenuOpen
                                    ? 'bg-teal-50 border-teal-300 text-teal-900 shadow-xs'
                                    : 'bg-white hover:bg-slate-50 border-slate-200 text-slate-700 shadow-xs'
                                }`}
                        >
                            <div className="w-7 h-7 rounded-lg bg-teal-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                                {user?.name ? user.name[0].toUpperCase() : 'U'}
                            </div>
                            <div className="text-left hidden sm:block">
                                <div className="text-xs font-bold leading-none truncate max-w-[100px]">
                                    {user?.name || 'My Account'}
                                </div>
                                <div className="text-[10px] text-slate-400 capitalize mt-0.5">
                                    {isDoctor ? 'Doctor' : 'Patient'}
                                </div>
                            </div>
                            <ChevronDown className={`w-3.5 h-3.5 text-slate-400 transition-transform duration-200 ${isProfileMenuOpen ? 'rotate-180' : ''}`} />
                        </button>

                        {/* Dropdown Card */}
                        {isProfileMenuOpen && (
                            <div className="absolute right-0 mt-2 w-64 bg-white rounded-2xl shadow-xl border border-slate-100 p-2 z-50 animate-fade-in space-y-1">

                                {/* Account Details Header */}
                                <div className="p-3 bg-slate-50 rounded-xl border border-slate-100/80 mb-1">
                                    <div className="flex items-center gap-2 text-xs font-bold text-slate-900 truncate">
                                        {isDoctor ? <Stethoscope className="w-3.5 h-3.5 text-teal-600 shrink-0" /> : <ShieldCheck className="w-3.5 h-3.5 text-teal-600 shrink-0" />}
                                        <span className="truncate">{user?.name || 'User Profile'}</span>
                                    </div>
                                    <div className="text-[11px] text-slate-500 truncate mt-0.5">{user?.email}</div>
                                </div>

                                {/* View Profile Action */}
                                <button
                                    onClick={() => {
                                        setActiveTab('profile');
                                        setIsProfileMenuOpen(false);
                                    }}
                                    className={`w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold transition cursor-pointer ${activeTab === 'profile'
                                            ? 'bg-teal-50 text-teal-800'
                                            : 'text-slate-700 hover:bg-slate-50 hover:text-slate-900'
                                        }`}
                                >
                                    <User className="w-4 h-4 text-teal-600" />
                                    {isDoctor ? 'Doctor Profile Settings' : 'Patient Health Profile'}
                                </button>

                                <div className="border-t border-slate-100 my-1"></div>

                                {/* Sign Out Button (Inside Profile at Bottom) */}
                                <button
                                    onClick={() => {
                                        setIsProfileMenuOpen(false);
                                        logout();
                                    }}
                                    className="w-full flex items-center gap-2.5 px-3 py-2 rounded-xl text-xs font-semibold text-rose-600 hover:bg-rose-50 active:bg-rose-100 transition cursor-pointer"
                                >
                                    <LogOut className="w-4 h-4 text-rose-600" />
                                    Sign Out
                                </button>

                            </div>
                        )}
                    </div>
                </div>

            </div>
        </header>
    );
};

export default Navbar;