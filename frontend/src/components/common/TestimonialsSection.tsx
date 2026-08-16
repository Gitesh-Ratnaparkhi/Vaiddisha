// frontend/src/components/common/TestimonialsSection.tsx
import React, { useState, useEffect } from 'react';
import { Star, Quote, ShieldCheck, ChevronLeft, ChevronRight, UserCheck, Stethoscope } from 'lucide-react';

interface Testimonial {
    id: number;
    name: string;
    role: 'Patient' | 'Doctor';
    title: string;
    city: string;
    avatar: string;
    rating: number;
    review: string;
    tag: string;
}

const TESTIMONIALS_DATA: Testimonial[] = [
    {
        id: 1,
        name: "Dr. Rajesh Kulkarni",
        role: "Doctor",
        title: "Senior Cardiologist",
        city: "Nagpur",
        avatar: "RK",
        rating: 5,
        tag: "Clinical Decision Support",
        review: "Vaiddisha AI's differential triage has significantly sped up our outpatient pre-screening. The clarity and precision of generated patient summaries are remarkable."
    },
    {
        id: 2,
        name: "Pooja Deshmukh",
        role: "Patient",
        title: "Recovered Patient",
        city: "Mumbai",
        avatar: "PD",
        rating: 5,
        tag: "Symptom Triage",
        review: "I described my persistent abdominal pains using the voice feature in Marathi. The AI accurately advised a gastroenterologist consultation, which helped me treat my condition early."
    },
    {
        id: 3,
        name: "Dr. Ananya Sen",
        role: "Doctor",
        title: "Endocrinologist",
        city: "Pune",
        avatar: "AS",
        rating: 5,
        tag: "Lab Vision OCR",
        review: "The OCR extraction for complex lipid and HbA1c panels saves immense documentation time. My patients come in well-prepared with structured biomarker timelines."
    },
    {
        id: 4,
        name: "Vikram Malhotra",
        role: "Patient",
        title: "Verified User",
        city: "Nagpur",
        avatar: "VM",
        rating: 5,
        tag: "Specialist Booking",
        review: "Finding certified local doctors by pin code and booking same-day consultations was effortless. The appointment updates are instant and reliable."
    }
];

export const TestimonialsSection: React.FC = () => {
    const [currentIndex, setCurrentIndex] = useState(0);
    const [filter, setFilter] = useState<'All' | 'Patient' | 'Doctor'>('All');
    const [isPaused, setIsPaused] = useState(false);

    const filteredData = TESTIMONIALS_DATA.filter(
        item => filter === 'All' || item.role === filter
    );

    // Auto-play animation interval
    useEffect(() => {
        if (isPaused || filteredData.length <= 1) return;

        const timer = setInterval(() => {
            setCurrentIndex(prev => (prev + 1) % filteredData.length);
        }, 4500);

        return () => clearInterval(timer);
    }, [isPaused, filteredData.length]);

    const handlePrev = () => {
        setCurrentIndex(prev => (prev === 0 ? filteredData.length - 1 : prev - 1));
    };

    const handleNext = () => {
        setCurrentIndex(prev => (prev + 1) % filteredData.length);
    };

    return (
        <section
            className="my-10 bg-gradient-to-b from-slate-50 to-white p-6 sm:p-10 rounded-3xl border border-slate-200/80 shadow-xs relative overflow-hidden"
            onMouseEnter={() => setIsPaused(true)}
            onMouseLeave={() => setIsPaused(false)}
        >
            {/* Background Decorative Circles */}
            <div className="absolute -top-12 -right-12 w-48 h-48 bg-teal-100/50 rounded-full blur-2xl pointer-events-none" />
            <div className="absolute -bottom-12 -left-12 w-48 h-48 bg-emerald-100/40 rounded-full blur-2xl pointer-events-none" />

            {/* Header & Category Filters */}
            <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8">
                <div>
                    <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-teal-50 border border-teal-200 text-teal-700 text-xs font-semibold mb-2">
                        <ShieldCheck className="w-3.5 h-3.5 text-teal-600" />
                        Verified Clinical Experiences
                    </div>
                    <h3 className="text-2xl font-bold text-slate-900 tracking-tight">
                        Trusted by Doctors & Patients Across India
                    </h3>
                    <p className="text-xs text-slate-500 mt-1 max-w-xl">
                        Real stories from clinicians enhancing their diagnosis speed and patients receiving timely medical guidance.
                    </p>
                </div>

                {/* Filter Pills */}
                <div className="flex items-center gap-1.5 bg-slate-100 p-1 rounded-xl text-xs font-semibold self-start md:self-auto">
                    {(['All', 'Patient', 'Doctor'] as const).map(role => (
                        <button
                            key={role}
                            onClick={() => {
                                setFilter(role);
                                setCurrentIndex(0);
                            }}
                            className={`px-3.5 py-1.5 rounded-lg transition-all ${filter === role
                                    ? 'bg-white text-teal-800 shadow-xs font-bold'
                                    : 'text-slate-600 hover:text-slate-900'
                                }`}
                        >
                            {role === 'All' ? 'All Reviews' : `${role}s`}
                        </button>
                    ))}
                </div>
            </div>

            {/* Carousel / Animated Cards Grid */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                {filteredData.map((item, idx) => {
                    const isActive = idx === currentIndex || (idx === (currentIndex + 1) % filteredData.length);

                    return (
                        <div
                            key={item.id}
                            className={`bg-white p-6 rounded-2xl border transition-all duration-500 flex flex-col justify-between relative shadow-xs ${isActive
                                    ? 'border-teal-200 ring-1 ring-teal-50 scale-[1.01] opacity-100'
                                    : 'border-slate-200 opacity-70 hover:opacity-100'
                                }`}
                        >
                            <div className="space-y-3.5">
                                {/* Top Badge & Rating */}
                                <div className="flex items-center justify-between">
                                    <span className="inline-flex items-center gap-1 text-[11px] font-semibold text-teal-700 bg-teal-50 px-2.5 py-0.5 rounded-md border border-teal-100">
                                        {item.role === 'Doctor' ? <Stethoscope className="w-3 h-3" /> : <UserCheck className="w-3 h-3" />}
                                        {item.tag}
                                    </span>
                                    <div className="flex items-center gap-0.5 text-amber-400">
                                        {[...Array(item.rating)].map((_, i) => (
                                            <Star key={i} className="w-3.5 h-3.5 fill-amber-400" />
                                        ))}
                                    </div>
                                </div>

                                {/* Review Text */}
                                <p className="text-xs text-slate-700 leading-relaxed italic relative">
                                    <Quote className="w-6 h-6 text-slate-200 absolute -top-2 -left-2 -z-0 opacity-60" />
                                    <span className="relative z-10">"{item.review}"</span>
                                </p>
                            </div>

                            {/* User Profile Footer */}
                            <div className="flex items-center gap-3 pt-4 mt-4 border-t border-slate-100">
                                <div className="w-10 h-10 rounded-xl bg-teal-600 text-white font-bold text-xs flex items-center justify-center shadow-xs">
                                    {item.avatar}
                                </div>
                                <div>
                                    <h5 className="font-bold text-slate-900 text-xs flex items-center gap-1">
                                        {item.name}
                                        <ShieldCheck className="w-3 h-3 text-teal-600" />
                                    </h5>
                                    <p className="text-[11px] text-slate-400">
                                        {item.title} • <span className="text-slate-500 font-medium">{item.city}</span>
                                    </p>
                                </div>
                            </div>
                        </div>
                    );
                })}
            </div>

            {/* Carousel Controls */}
            <div className="flex items-center justify-between mt-6 pt-4 border-t border-slate-100">
                <div className="flex items-center gap-1.5">
                    {filteredData.map((_, dotIdx) => (
                        <button
                            key={dotIdx}
                            onClick={() => setCurrentIndex(dotIdx)}
                            className={`h-1.5 rounded-full transition-all duration-300 ${currentIndex === dotIdx ? 'w-6 bg-teal-600' : 'w-2 bg-slate-200'
                                }`}
                            aria-label={`Go to slide ${dotIdx + 1}`}
                        />
                    ))}
                </div>

                <div className="flex items-center gap-2">
                    <button
                        onClick={handlePrev}
                        className="p-2 rounded-xl border border-slate-200 hover:bg-slate-100 text-slate-600 transition"
                        aria-label="Previous review"
                    >
                        <ChevronLeft className="w-4 h-4" />
                    </button>
                    <button
                        onClick={handleNext}
                        className="p-2 rounded-xl border border-slate-200 hover:bg-slate-100 text-slate-600 transition"
                        aria-label="Next review"
                    >
                        <ChevronRight className="w-4 h-4" />
                    </button>
                </div>
            </div>
        </section>
    );
};

export default TestimonialsSection;