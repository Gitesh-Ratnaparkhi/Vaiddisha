// frontend/src/components/common/WelcomeHero.tsx
import React, { useState } from 'react';
import { Sparkles, ArrowRight, ShieldCheck, Activity, Stethoscope, ChevronRight } from 'lucide-react';
import { Button } from './Button';

interface WelcomeHeroProps {
    onExploreTriage?: () => void;
    onExploreSpecialists?: () => void;
}

export const WelcomeHero: React.FC<WelcomeHeroProps> = ({
    onExploreTriage,
    onExploreSpecialists
}) => {
    const [activeTopic, setActiveTopic] = useState<'cardio' | 'lifestyle' | 'ocr'>('cardio');

    const topics = {
        cardio: {
            tag: "FEATURED CLINICAL INSIGHT",
            title: "Understanding Cardiovascular Risk & Early Triage",
            desc: "Cardiovascular conditions remain the leading cause of preventable critical care visits. Learn how early symptom recognition, blood pressure monitoring, and timely cardiology consultations can prevent acute coronary events.",
            imgUrl: "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=900&q=80",
            badge: "Clinical Cardiology",
            actionText: "Explore Heart Health Check",
            action: onExploreTriage
        },
        ocr: {
            tag: "INNOVATION SPOTLIGHT",
            title: "Automated Lab Vision OCR Interpretation",
            desc: "Upload CBC, Lipid, HbA1c, and Metabolic panel test reports. Vaiddisha AI accurately extracts complex biomarker parameters and highlights critical reference deviations instantly.",
            imgUrl: "https://images.unsplash.com/photo-1579154204601-01588f351e67?auto=format&fit=crop&w=900&q=80",
            badge: "Diagnostic AI",
            actionText: "Try Lab Vision OCR",
            action: onExploreTriage
        },
        lifestyle: {
            tag: "PREVENTIVE HEALTHCARE",
            title: "Seasonal Fever & Infection Management",
            desc: "Distinguish between common viral flus, dengue, and acute bacterial infections. Learn key red flag signs, proper hydration protocols, and when to seek urgent specialist intervention.",
            imgUrl: "https://images.unsplash.com/photo-1584515979956-d9f6e5d09982?auto=format&fit=crop&w=900&q=80",
            badge: "Internal Medicine",
            actionText: "Find Nearest Specialist",
            action: onExploreSpecialists
        }
    };

    const current = topics[activeTopic];

    return (
        <section className="bg-white rounded-3xl border border-slate-200/80 p-6 sm:p-8 shadow-xs mb-8 space-y-6">

            {/* Top Header & Platform Description */}
            <div className="border-b border-slate-100 pb-5 space-y-2">
                <div className="flex items-center gap-2">
                    <div className="w-8 h-8 rounded-xl bg-teal-50 text-teal-700 flex items-center justify-center font-bold text-sm border border-teal-100 shadow-xs">
                        ⚕️
                    </div>
                    <h2 className="text-2xl font-extrabold text-slate-900 tracking-tight">
                        Welcome to <span className="text-teal-600">Vaiddisha AI</span>
                    </h2>
                </div>
                <p className="text-xs sm:text-sm text-slate-600 leading-relaxed max-w-4xl">
                    Vaiddisha AI is an intelligent clinical decision support platform built for patients, families, and healthcare providers. It delivers instant AI-assisted differential diagnosis triage, automated lab report OCR vision analysis, and seamless booking with certified medical specialists.{' '}
                    <button
                        type="button"
                        onClick={onExploreTriage}
                        className="text-teal-600 hover:text-teal-800 font-bold hover:underline inline-flex items-center gap-0.5"
                    >
                        Learn more about Vaiddisha AI <ChevronRight className="w-3.5 h-3.5 inline" />
                    </button>
                </p>
            </div>

            {/* Featured Topic Card Layout (Image on Left, Content on Right) */}
            <div className="grid grid-cols-1 md:grid-cols-12 gap-6 lg:gap-8 items-center bg-slate-50/60 p-4 sm:p-6 rounded-2xl border border-slate-100">

                {/* Left Column: Image Card with Badge */}
                <div className="md:col-span-5 relative group overflow-hidden rounded-2xl shadow-xs border border-slate-200/80">
                    <img
                        src={current.imgUrl}
                        alt={current.title}
                        className="w-full h-56 sm:h-64 object-cover object-center group-hover:scale-105 transition-transform duration-500"
                    />
                    <div className="absolute top-3 left-3 bg-slate-900/80 backdrop-blur-xs text-white text-[10px] font-bold uppercase tracking-wider px-3 py-1 rounded-lg border border-white/20">
                        {current.badge}
                    </div>
                </div>

                {/* Right Column: Title, Description & Action Button */}
                <div className="md:col-span-7 space-y-4 flex flex-col justify-between">
                    <div className="space-y-2">
                        <span className="text-[11px] font-extrabold uppercase tracking-widest text-teal-700 bg-teal-50 px-2.5 py-1 rounded-md border border-teal-100 inline-block">
                            {current.tag}
                        </span>
                        <h3 className="text-xl sm:text-2xl font-bold text-slate-900 tracking-tight leading-snug">
                            {current.title}
                        </h3>
                        <p className="text-xs sm:text-sm text-slate-600 leading-relaxed">
                            {current.desc}
                        </p>
                    </div>

                    {/* Action Button & Topic Selector Tabs */}
                    <div className="pt-2 flex flex-wrap items-center justify-between gap-3 border-t border-slate-200/60">
                        <Button
                            variant="outline"
                            onClick={current.action}
                            className="px-5 py-2 text-xs font-bold border-teal-600 text-teal-700 hover:bg-teal-50 hover:border-teal-700 shadow-xs"
                            rightIcon={<ArrowRight className="w-3.5 h-3.5 text-teal-600" />}
                        >
                            {current.actionText}
                        </Button>

                        {/* Quick Topic Switcher Pills */}
                        <div className="flex items-center gap-1.5 text-[11px] font-semibold text-slate-500">
                            <span className="text-[10px] uppercase text-slate-400">Insights:</span>
                            {(['cardio', 'ocr', 'lifestyle'] as const).map((key) => (
                                <button
                                    key={key}
                                    onClick={() => setActiveTopic(key)}
                                    className={`px-2.5 py-1 rounded-lg transition-all capitalize cursor-pointer ${activeTopic === key
                                            ? 'bg-teal-600 text-white font-bold shadow-xs'
                                            : 'bg-white hover:bg-slate-200/80 text-slate-600 border border-slate-200'
                                        }`}
                                >
                                    {key === 'cardio' ? 'Cardio' : key === 'ocr' ? 'Lab OCR' : 'Seasonal'}
                                </button>
                            ))}
                        </div>
                    </div>

                </div>

            </div>

        </section>
    );
};

export default WelcomeHero;