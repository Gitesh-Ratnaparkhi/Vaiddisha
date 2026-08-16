// frontend/src/components/common/TermsModal.tsx
import React from 'react';
import { X, ShieldCheck, FileText } from 'lucide-react';
import { Button } from './Button';

interface TermsModalProps {
    isOpen: boolean;
    onClose: () => void;
}

export const TermsModal: React.FC<TermsModalProps> = ({ isOpen, onClose }) => {
    if (!isOpen) return null;

    return (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-900/50 backdrop-blur-xs p-4 animate-fade-in">
            <div className="bg-white max-w-lg w-full rounded-3xl p-6 sm:p-8 shadow-2xl border border-slate-200 flex flex-col max-h-[85vh] space-y-4">

                {/* Modal Header */}
                <div className="flex items-center justify-between border-b border-slate-100 pb-3">
                    <div className="flex items-center gap-2.5">
                        <div className="w-9 h-9 rounded-xl bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-100 shadow-xs">
                            <FileText className="w-5 h-5" />
                        </div>
                        <div>
                            <h3 className="text-base font-bold text-slate-900">Terms & Conditions</h3>
                            <p className="text-[11px] text-slate-400">Clinical decision support usage agreement</p>
                        </div>
                    </div>
                    <button
                        onClick={onClose}
                        className="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 hover:bg-slate-100 transition cursor-pointer"
                    >
                        <X className="w-5 h-5" />
                    </button>
                </div>

                {/* Scrollable Terms Content */}
                <div className="flex-1 overflow-y-auto pr-2 text-xs text-slate-600 leading-relaxed space-y-3.5 border-b border-slate-100 pb-4">
                    <div className="p-3 bg-teal-50/70 border border-teal-200/60 rounded-xl text-teal-900 flex items-start gap-2">
                        <ShieldCheck className="w-4 h-4 text-teal-600 shrink-0 mt-0.5" />
                        <p className="text-[11px] leading-normal font-medium">
                            By registering an account with Vaiddisha AI, you acknowledge that our algorithms provide clinical decision support and preliminary triage guidance, not definitive diagnoses.
                        </p>
                    </div>

                    <div>
                        <h4 className="font-bold text-slate-900 mb-1">1. Educational & Preliminary Nature</h4>
                        <p>
                            Vaiddisha AI uses AI language models and optical character recognition to organize symptom descriptions and lab reports. It does not replace a physical medical exam by a registered doctor.
                        </p>
                    </div>

                    <div>
                        <h4 className="font-bold text-slate-900 mb-1">2. Emergency Medical Conditions</h4>
                        <p>
                            In life-threatening situations (e.g., severe chest pain, stroke symptoms, acute breathing distress), call national emergency helplines (<strong>112 / 108</strong>) or visit an emergency trauma center immediately.
                        </p>
                    </div>

                    <div>
                        <h4 className="font-bold text-slate-900 mb-1">3. Privacy & Clinical Record Security</h4>
                        <p>
                            Your health data and uploaded documents are handled in compliance with HIPAA and GDPR data minimization standards. Data is protected with 256-bit SSL encryption.
                        </p>
                    </div>

                    <div>
                        <h4 className="font-bold text-slate-900 mb-1">4. Specialist Consultations</h4>
                        <p>
                            Appointments scheduled through our directory connect you with independent certified practitioners. Clinical recommendations made during consultations are the responsibility of the consulting physician.
                        </p>
                    </div>
                </div>

                {/* Modal Footer */}
                <div className="flex justify-end pt-1">
                    <Button variant="primary" onClick={onClose} className="px-6 py-2 text-xs">
                        I Understand & Agree
                    </Button>
                </div>

            </div>
        </div>
    );
};

export default TermsModal;