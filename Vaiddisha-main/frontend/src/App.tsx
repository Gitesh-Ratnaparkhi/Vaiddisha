// frontend/src/App.tsx
import { useState, useEffect } from 'react';
import { useAuth } from './hooks/useAuth';
import Navbar, { type TabType } from './components/layout/Navbar';
import Footer from './components/layout/Footer';
import AuthModal from './components/common/AuthModal';
import PrivacyPolicyModal from './components/common/PrivacyPolicyModal';
import SymptomChecker from './pages/SymptomChecker';
import LabAnalyzer from './pages/LabAnalyzer';
import DoctorDirectory from './pages/DoctorDirectory';
import Appointments from './pages/Appointments';
import Profile from './pages/Profile';
import {
  ShieldCheck,
  Sparkles,
  ArrowRight,
  Lock,
  Stethoscope,
  FileSearch,
  CalendarCheck2
} from 'lucide-react';

export const App = () => {
  const { user } = useAuth();
  const isDoctor = user?.role?.toLowerCase() === 'doctor';
  const [activeTab, setActiveTab] = useState<TabType>('triage');
  const [isAuthModalOpen, setIsAuthModalOpen] = useState(false);
  const [isPrivacyOpen, setIsPrivacyOpen] = useState(false);

  // Automatically route doctor to Appointments on login
  useEffect(() => {
    if (isDoctor && (activeTab === 'triage' || activeTab === 'lab' || activeTab === 'doctors')) {
      setActiveTab('appointments');
    }
  }, [user, isDoctor]);

  // Enhanced Interactive Authentication Gate
  if (!user) {
    return (
      <div className="min-h-screen relative flex flex-col justify-between overflow-hidden bg-slate-50 selection:bg-teal-500 selection:text-white">

        {/* Animated Background Mesh Orbs */}
        <div className="fixed top-10 left-1/4 w-96 h-96 bg-teal-300/25 rounded-full blur-3xl pointer-events-none animate-pulse-glow -z-10" />
        <div className="fixed bottom-10 right-1/4 w-96 h-96 bg-sky-300/25 rounded-full blur-3xl pointer-events-none animate-pulse-glow -z-10" />
        <div className="fixed top-1/2 left-10 w-80 h-80 bg-emerald-200/20 rounded-full blur-3xl pointer-events-none -z-10" />

        {/* Minimal Header */}
        <header className="max-w-7xl mx-auto w-full px-6 py-6 flex items-center justify-between z-10">
          <div className="flex items-center gap-3 select-none">
            <div className="w-10 h-10 rounded-2xl bg-gradient-to-tr from-teal-700 to-teal-500 flex items-center justify-center text-white font-bold shadow-md shadow-teal-600/20">
              ⚕️
            </div>
            <div>
              <div className="text-xl font-bold text-slate-900 tracking-tight">
                Vaiddisha <span className="text-teal-600">AI</span>
              </div>
              <div className="text-[10px] uppercase font-bold tracking-wider text-slate-400">
                Clinical Decision Support
              </div>
            </div>
          </div>

          <div className="flex items-center gap-2 text-xs font-semibold text-teal-800 bg-teal-50/80 border border-teal-200/60 px-3.5 py-1.5 rounded-xl shadow-xs">
            <ShieldCheck className="w-4 h-4 text-teal-600" />
            HIPAA & GDPR Compliant
          </div>
        </header>

        {/* Center Hero Card */}
        <main className="flex-1 flex items-center justify-center p-4 sm:p-6 z-10">
          <div className="max-w-xl w-full bg-white/95 backdrop-blur-md rounded-3xl p-8 sm:p-10 shadow-xl border border-slate-200/80 text-center space-y-6 animate-fade-in relative">

            {/* Top Glowing Emblem */}
            <div className="relative mx-auto w-20 h-20">
              <div className="absolute inset-0 bg-teal-400/30 rounded-3xl blur-md animate-pulse" />
              <div className="relative w-20 h-20 bg-gradient-to-br from-teal-50 to-teal-100/80 rounded-3xl border border-teal-200/80 flex items-center justify-center text-3xl shadow-xs animate-float">
                ⚕️
              </div>
            </div>

            {/* Title & Description */}
            <div className="space-y-2">
              <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-teal-700 text-[11px] font-bold uppercase tracking-wider">
                <Sparkles className="w-3.5 h-3.5" /> Clinical Portal Security
              </div>
              <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
                Patient & Provider Access
              </h1>
              <p className="text-xs sm:text-sm text-slate-500 max-w-md mx-auto leading-relaxed">
                Sign in to consult the AI clinical differential triage engine, inspect lab vision biomarkers, and schedule verified specialist consultations.
              </p>
            </div>

            {/* Quick Feature Highlights */}
            <div className="grid grid-cols-3 gap-2.5 py-3 border-y border-slate-100 text-slate-700">
              <div className="flex flex-col items-center gap-1 p-2 rounded-xl bg-slate-50 border border-slate-100">
                <Stethoscope className="w-4 h-4 text-teal-600" />
                <span className="text-[11px] font-bold">AI Triage</span>
              </div>
              <div className="flex flex-col items-center gap-1 p-2 rounded-xl bg-slate-50 border border-slate-100">
                <FileSearch className="w-4 h-4 text-teal-600" />
                <span className="text-[11px] font-bold">Lab Vision OCR</span>
              </div>
              <div className="flex flex-col items-center gap-1 p-2 rounded-xl bg-slate-50 border border-slate-100">
                <CalendarCheck2 className="w-4 h-4 text-teal-600" />
                <span className="text-[11px] font-bold">Specialists</span>
              </div>
            </div>

            {/* Primary Action Button */}
            <button
              onClick={() => setIsAuthModalOpen(true)}
              className="w-full py-3.5 px-6 bg-gradient-to-r from-teal-600 to-teal-700 hover:from-teal-700 hover:to-teal-800 text-white font-bold rounded-2xl shadow-md shadow-teal-600/25 transition-all duration-200 cursor-pointer active:scale-[0.98] flex items-center justify-center gap-2 group text-sm"
            >
              <Lock className="w-4 h-4 text-teal-200 group-hover:scale-110 transition-transform" />
              <span>Sign In / Register Account</span>
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>

            {/* Clinical Security Notice */}
            <p className="text-[11px] text-slate-400">
              Encrypted patient records • 256-bit SSL Clinical Safety Architecture
            </p>
          </div>
        </main>

        {/* Minimal Footer */}
        <footer className="py-4 text-center text-xs text-slate-400 border-t border-slate-200/60 z-10">
          © {new Date().getFullYear()} Vaiddisha AI • Intelligent Healthcare Decision Support
        </footer>

        {/* Modal Sheet */}
        {isAuthModalOpen && (
          <AuthModal
            onClose={() => setIsAuthModalOpen(false)}
            onLoginSuccess={() => setIsAuthModalOpen(false)}
          />
        )}
      </div>
    );
  }

  return (
    <div className="min-h-screen relative flex flex-col overflow-x-hidden">
      {/* Decorative Ambient Background Lights */}
      <div className="fixed top-0 left-1/4 w-96 h-96 bg-teal-200/20 rounded-full blur-3xl pointer-events-none -z-10" />
      <div className="fixed top-1/3 right-10 w-80 h-80 bg-sky-200/20 rounded-full blur-3xl pointer-events-none -z-10" />
      <div className="fixed bottom-32 left-10 w-80 h-80 bg-emerald-100/30 rounded-full blur-3xl pointer-events-none -z-10" />

      {/* Top Navigation Bar */}
      <Navbar activeTab={activeTab} setActiveTab={setActiveTab} />

      {/* Main Page Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 sm:p-6 lg:p-8">
        {!isDoctor && activeTab === 'triage' && <SymptomChecker />}
        {!isDoctor && activeTab === 'lab' && <LabAnalyzer />}
        {!isDoctor && activeTab === 'doctors' && <DoctorDirectory />}
        {activeTab === 'appointments' && (
          <Appointments onNavigateToDirectory={() => setActiveTab('doctors')} />
        )}
        {activeTab === 'profile' && <Profile />}
      </main>

      {/* Persistent Bottom Footer */}
      <Footer
        setActiveTab={setActiveTab}
        isDoctor={isDoctor}
        onOpenPrivacyPolicy={() => setIsPrivacyOpen(true)}
      />

      {/* Privacy Policy Modal */}
      <PrivacyPolicyModal
        isOpen={isPrivacyOpen}
        onClose={() => setIsPrivacyOpen(false)}
      />
    </div>
  );
};

export default App;