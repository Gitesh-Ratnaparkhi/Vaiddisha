// frontend/src/components/common/PrivacyPolicyModal.tsx
import React from 'react';
import { X, Shield, Lock, Eye, Database, FileText, CheckCircle2 } from 'lucide-react';

interface PrivacyPolicyModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const PrivacyPolicyModal: React.FC<PrivacyPolicyModalProps> = ({ isOpen, onClose }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/60 backdrop-blur-xs p-4 animate-fade-in">
            <div className="bg-white w-full max-w-3xl rounded-2xl shadow-2xl border border-slate-200 flex flex-col max-h-[85vh] overflow-hidden">

                {/* Modal Header */}
                <div className="p-6 border-b border-slate-100 flex items-center justify-between bg-slate-50/50">
                    <div className="flex items-center gap-3">
                        <div className="w-10 h-10 rounded-xl bg-teal-100 text-teal-700 flex items-center justify-center">
                            <Shield className="w-5 h-5" />
                        </div>
                        <div>
                            <h2 className="text-lg font-bold text-slate-900">Privacy Policy & Health Data Protection</h2>
                            <p className="text-xs text-slate-500">Last updated: August 2026 • Version 1.2</p>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-2 text-slate-400 hover:text-slate-600 rounded-xl hover:bg-slate-100 transition"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Modal Content */}
                <div className="p-6 overflow-y-auto space-y-6 text-slate-600 text-xs leading-relaxed">

                    <section className="space-y-2">
                        <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                            <Lock className="w-4 h-4 text-teal-600" /> 1. Commitment to Health Data Security
                        </h3>
                        <p>
                            At <strong>Vaiddisha AI</strong>, protecting your Sensitive Personal Data or Information (SPDI) and Protected Health Information (PHI) is our highest clinical priority. This Privacy Policy governs the manner in which we collect, encrypt, analyze, and safeguard health data provided through our clinical decision-support portal.
                        </p>
                    </section>

                    <section className="space-y-2">
                        <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                            <Database className="w-4 h-4 text-teal-600" /> 2. Information We Collect
                        </h3>
                        <ul className="list-disc pl-5 space-y-1">
                            <li><strong>Patient Health Data:</strong> Reported medical symptoms, health condition history, known drug allergies, surgical histories, and uploaded lab report images/PDFs.</li>
                            <li><strong>Doctor & Provider Details:</strong> Medical council registration details, qualifications, clinical specializations, clinic addresses, and consultation fee schedules.</li>
                            <li><strong>Technical Metadata:</strong> Encrypted authentication tokens, session timestamps, and device diagnostics strictly for security auditing.</li>
                        </ul>
                    </section>

                    <section className="space-y-2">
                        <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                            <Eye className="w-4 h-4 text-teal-600" /> 3. How We Use Clinical & AI Data
                        </h3>
                        <p>
                            Data entered into the <strong>Symptom Triage</strong> and <strong>Lab Vision OCR</strong> engines are processed using high-security inference APIs.
                        </p>
                        <ul className="list-disc pl-5 space-y-1">
                            <li>Your data is used solely to generate differential diagnostic reports and match relevant medical specialists.</li>
                            <li><strong>Zero Permanent Training on PHI:</strong> Patient symptom narrations and uploaded medical files are not used to publicly train public LLMs.</li>
                            <li>Clinical report summaries are shared exclusively with the certified doctor you choose to book an appointment with.</li>
                        </ul>
                    </section>

                    <section className="space-y-2">
                        <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                            <CheckCircle2 className="w-4 h-4 text-teal-600" /> 4. Regulatory Compliance & Encryption Standards
                        </h3>
                        <p>
                            Our backend database and communication protocols adhere to the following standards:
                        </p>
                        <ul className="list-disc pl-5 space-y-1">
                            <li><strong>Digital Personal Data Protection Act (DPDPA), India:</strong> Explicit user consent for processing personal health records.</li>
                            <li><strong>Encryption at Rest & In Transit:</strong> All HTTP traffic is protected via TLS 1.3 encryption, and database credentials are fully salted with cryptographic hashing.</li>
                            <li><strong>Role-Based Access Control (RBAC):</strong> Doctor accounts are restricted from accessing unassigned patient health records.</li>
                        </ul>
                    </section>

                    <section className="space-y-2">
                        <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                            <FileText className="w-4 h-4 text-teal-600" /> 5. Data Retention and Right to Deletion
                        </h3>
                        <p>
                            Users hold complete data sovereignty. You may request permanent deletion of your clinical reports, appointment logs, and user profile at any time by contacting <span className="text-teal-600 font-semibold">privacy@vaiddisha.ai</span>.
                        </p>
                    </section>

                </div>

                {/* Modal Footer */}
                <div className="p-4 border-t border-slate-100 bg-slate-50 flex items-center justify-between">
                    <span className="text-[11px] text-slate-400">Vaiddisha AI Health Data Governance</span>
                    <button
                        onClick={onClose}
                        className="px-5 py-2 bg-teal-600 hover:bg-teal-700 text-white rounded-xl text-xs font-semibold shadow-xs transition"
                    >
                        I Understand & Agree
                    </button>
                </div>

            </div>
        </div>
    );
};

export default PrivacyPolicyModal;