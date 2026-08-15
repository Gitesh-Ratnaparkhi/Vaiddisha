// frontend/src/App.tsx
import { useState } from 'react';
import {
  Activity,
  Stethoscope,
  FileText,
  Calendar,
  UserCheck
} from 'lucide-react';
import { AuthModal } from './components/common';
import SymptomChecker from './pages/SymptomChecker.tsx';
import LabAnalyzer from './pages/LabAnalyzer.tsx';
import DoctorDirectory from './pages/DoctorDirectory.tsx';
import Appointments from './pages/Appointments.tsx';
import { useAuth } from './hooks/useAuth';

export default function App() {
  const [activeTab, setActiveTab] = useState<'checker' | 'lab' | 'doctors' | 'appointments'>('checker');
  const [showAuthModal, setShowAuthModal] = useState(false);
  const { user, logout } = useAuth();

  return (
    <div className="min-h-screen bg-slate-50 text-slate-900 flex flex-col font-sans">
      {/* Top Header */}
      <header className="sticky top-0 z-40 bg-white/90 backdrop-blur border-b border-slate-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-teal-600 flex items-center justify-center text-white shadow-md shadow-teal-500/20">
              <Activity className="w-6 h-6" />
            </div>
            <div>
              <h1 className="text-xl font-bold bg-gradient-to-r from-teal-700 to-emerald-600 bg-clip-text text-transparent">
                Vaiddisha AI
              </h1>
              <p className="text-xs text-slate-500 font-medium">Clinical Decision-Support & Doctor Portal</p>
            </div>
          </div>

          {/* Nav Tabs */}
          <nav className="flex items-center gap-1 bg-slate-100 p-1 rounded-xl border border-slate-200/80">
            <button
              onClick={() => setActiveTab('checker')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition ${activeTab === 'checker' ? 'bg-white text-teal-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                }`}
            >
              <Stethoscope className="w-4 h-4" />
              Symptom Triage
            </button>
            <button
              onClick={() => setActiveTab('lab')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition ${activeTab === 'lab' ? 'bg-white text-teal-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                }`}
            >
              <FileText className="w-4 h-4" />
              Lab Vision OCR
            </button>
            <button
              onClick={() => setActiveTab('doctors')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition ${activeTab === 'doctors' ? 'bg-white text-teal-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                }`}
            >
              <UserCheck className="w-4 h-4" />
              Specialists
            </button>
            <button
              onClick={() => setActiveTab('appointments')}
              className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition ${activeTab === 'appointments' ? 'bg-white text-teal-700 shadow-sm' : 'text-slate-600 hover:text-slate-900'
                }`}
            >
              <Calendar className="w-4 h-4" />
              Appointments
            </button>
          </nav>

          {/* Auth Button / Profile */}
          <div>
            {user ? (
              <div className="flex items-center gap-3">
                <div className="text-right">
                  <p className="text-xs font-bold text-slate-800">{user.email}</p>
                  <span className="text-[10px] uppercase tracking-wider font-semibold text-teal-600 bg-teal-50 px-2 py-0.5 rounded-full">
                    {user.role}
                  </span>
                </div>
                <button
                  onClick={logout}
                  className="text-xs text-rose-600 hover:underline font-medium"
                >
                  Logout
                </button>
              </div>
            ) : (
              <button
                onClick={() => setShowAuthModal(true)}
                className="px-4 py-2 bg-teal-600 hover:bg-teal-700 text-white rounded-lg text-sm font-medium shadow-sm transition"
              >
                Sign In / Register
              </button>
            )}
          </div>
        </div>
      </header>

      {/* Main Tab Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto p-4 md:p-6">
        {activeTab === 'checker' && <SymptomChecker userSession={user} />}
        {activeTab === 'lab' && <LabAnalyzer />}
        {activeTab === 'doctors' && <DoctorDirectory />}
        {activeTab === 'appointments' && <Appointments />}
      </main>

      {/* Auth Modal */}
      {showAuthModal && (
        <AuthModal
          onClose={() => setShowAuthModal(false)}
          onLoginSuccess={() => setShowAuthModal(false)}
        />
      )}
    </div>
  );
}