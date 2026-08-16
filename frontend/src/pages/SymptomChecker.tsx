// frontend/src/pages/SymptomChecker.tsx
import React, { useState, useEffect, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import ReactMarkdown from 'react-markdown';
import { triageApi, API_BASE_URL } from '../api';
import { useToast } from '../context/ToastContext';
import { useAuth } from '../hooks/useAuth';
import type { TriageQuestion } from '../types';
import { Button } from '../components/common/Button';
import { WelcomeHero } from '../components/common/WelcomeHero';
import { TestimonialsSection } from '../components/common/TestimonialsSection';
import {
    Stethoscope,
    ArrowRight,
    ArrowLeft,
    Sparkles,
    FileText,
    Download,
    RefreshCw,
    AlertCircle,
    CheckCircle,
    HelpCircle,
    Globe,
    Mic,
    Square,
    Volume2
} from 'lucide-react';

export const SymptomChecker: React.FC = () => {
    const { t, i18n } = useTranslation();
    const { user } = useAuth();
    const { showToast } = useToast();

    // Step state: 'input' | 'questions' | 'result'
    const [step, setStep] = useState<'input' | 'questions' | 'result'>('input');
    const [symptoms, setSymptoms] = useState('');
    const [targetLanguage, setTargetLanguage] = useState(i18n.language === 'hi' ? 'Hindi' : 'English');
    const [questions, setQuestions] = useState<TriageQuestion[]>([]);
    const [answers, setAnswers] = useState<Record<string, string>>({});
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<{ analysis_markdown: string; pdf_download_path: string } | null>(null);

    // Speech Recognition & Web Audio Visualizer State
    const [isListening, setIsListening] = useState(false);
    const [audioVolume, setAudioVolume] = useState<number>(0);
    const recognitionRef = useRef<any>(null);
    const audioContextRef = useRef<AudioContext | null>(null);
    const mediaStreamRef = useRef<MediaStream | null>(null);
    const animationFrameRef = useRef<number | null>(null);

    // Keep target report language synced when global i18n changes
    useEffect(() => {
        setTargetLanguage(i18n.language === 'hi' ? 'Hindi' : 'English');
    }, [i18n.language]);

    const languages = [
        { code: 'en', name: 'English (English)', langLabel: 'English', speechLang: 'en-IN' },
        { code: 'hi', name: 'हिंदी (Hindi)', langLabel: 'Hindi', speechLang: 'hi-IN' },
        { code: 'mr', name: 'मराठी (Marathi)', langLabel: 'Marathi', speechLang: 'mr-IN' },
        { code: 'es', name: 'Español (Spanish)', langLabel: 'Spanish', speechLang: 'es-ES' }
    ];

    const handleLanguageSelect = (langCode: string, langName: string) => {
        i18n.changeLanguage(langCode);
        localStorage.setItem('app_lang', langCode);
        setTargetLanguage(langName);
    };

    // Cleanup audio resources when unmounting or stopping
    const stopAudioStream = () => {
        if (animationFrameRef.current) {
            cancelAnimationFrame(animationFrameRef.current);
        }
        if (mediaStreamRef.current) {
            mediaStreamRef.current.getTracks().forEach(track => track.stop());
            mediaStreamRef.current = null;
        }
        if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
            audioContextRef.current.close();
            audioContextRef.current = null;
        }
        setAudioVolume(0);
    };

    // Toggle Voice-to-Text Input with Real-time Audio Visualizer
    const toggleVoiceInput = async () => {
        const SpeechRecognition = (window as any).SpeechRecognition || (window as any).webkitSpeechRecognition;

        if (!SpeechRecognition) {
            showToast('Speech recognition is not supported in this browser. Please use Chrome, Edge, or Safari.', 'error');
            return;
        }

        if (isListening) {
            recognitionRef.current?.stop();
            stopAudioStream();
            setIsListening(false);
            return;
        }

        try {
            // Setup Web Audio Stream for Volume Detection & Visual Waves
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaStreamRef.current = stream;

            const AudioContextClass = window.AudioContext || (window as any).webkitAudioContext;
            const audioCtx = new AudioContextClass();
            audioContextRef.current = audioCtx;

            const source = audioCtx.createMediaStreamSource(stream);
            const analyser = audioCtx.createAnalyser();
            analyser.fftSize = 64;
            source.connect(analyser);

            const dataArray = new Uint8Array(analyser.frequencyBinCount);

            const checkVolume = () => {
                analyser.getByteFrequencyData(dataArray);
                const average = dataArray.reduce((acc, val) => acc + val, 0) / dataArray.length;
                setAudioVolume(Math.min(100, Math.round((average / 128) * 100)));
                animationFrameRef.current = requestAnimationFrame(checkVolume);
            };
            checkVolume();

            // Setup Speech Recognition
            const currentLangObj = languages.find(l => l.code === i18n.language) || languages[0];
            const recognition = new SpeechRecognition();
            recognition.lang = currentLangObj.speechLang;
            recognition.continuous = true;
            recognition.interimResults = true;

            recognition.onstart = () => {
                setIsListening(true);
                showToast(`Listening in ${currentLangObj.langLabel}... Speak now`, 'info');
            };

            recognition.onresult = (event: any) => {
                let interimTranscript = '';
                let finalTranscript = '';

                for (let i = event.resultIndex; i < event.results.length; ++i) {
                    if (event.results[i].isFinal) {
                        finalTranscript += event.results[i][0].transcript;
                    } else {
                        interimTranscript += event.results[i][0].transcript;
                    }
                }

                if (finalTranscript) {
                    setSymptoms(prev => (prev ? `${prev} ${finalTranscript}` : finalTranscript));
                }
            };

            recognition.onerror = (event: any) => {
                console.error('Speech recognition error:', event.error);
                stopAudioStream();
                setIsListening(false);
                if (event.error !== 'no-speech') {
                    showToast('Microphone access denied or speech interrupted.', 'error');
                }
            };

            recognition.onend = () => {
                stopAudioStream();
                setIsListening(false);
            };

            recognitionRef.current = recognition;
            recognition.start();

        } catch (err) {
            console.error('Microphone permission error:', err);
            showToast('Please grant microphone permission in your browser.', 'error');
            setIsListening(false);
            stopAudioStream();
        }
    };

    // Stage 1: Get follow-up questions based on symptoms
    const handleStartTriage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (isListening) {
            recognitionRef.current?.stop();
            stopAudioStream();
            setIsListening(false);
        }

        if (!symptoms.trim()) {
            showToast('Please describe your symptoms to begin.', 'error');
            return;
        }

        setLoading(true);
        try {
            const res = await triageApi.getQuestions({ symptoms });
            if (res.questions && res.questions.length > 0) {
                setQuestions(res.questions);
                const initialAnswers: Record<string, string> = {};
                res.questions.forEach((q: TriageQuestion) => {
                    initialAnswers[q.id] = '';
                });
                setAnswers(initialAnswers);
                setStep('questions');
                showToast('Follow-up questions generated successfully.', 'success');
            } else {
                await handlePredictDiagnosis(true);
            }
        } catch (err: any) {
            showToast(err.message || 'Failed to initialize symptom triage.', 'error');
        } finally {
            setLoading(false);
        }
    };

    // Stage 2: Predict diagnosis based on initial symptoms & triage answers
    const handlePredictDiagnosis = async (skipQuestions = false) => {
        setLoading(true);
        try {
            let formattedAnswers = '';
            if (!skipQuestions && questions.length > 0) {
                const answerList = questions
                    .map(q => {
                        const ans = answers[q.id];
                        return ans ? `${q.question}: ${ans}` : null;
                    })
                    .filter(Boolean);
                formattedAnswers = answerList.join(' | ');
            }

            const res = await triageApi.predictDiagnosis({
                symptoms,
                triage_answers: formattedAnswers || undefined,
                patient_email: user?.email || undefined,
                target_language: targetLanguage
            });

            if (res.status === 'success') {
                setResult({
                    analysis_markdown: res.analysis_markdown,
                    pdf_download_path: res.pdf_download_path
                });
                setStep('result');
                showToast('Diagnostic assessment completed!', 'success');
            } else {
                throw new Error('Unsuccessful diagnostic prediction response.');
            }
        } catch (err: any) {
            showToast(err.message || 'Failed to retrieve AI clinical assessment.', 'error');
        } finally {
            setLoading(false);
        }
    };

    const handleAnswerChange = (questionId: string, value: string) => {
        setAnswers(prev => ({
            ...prev,
            [questionId]: value
        }));
    };

    const handleReset = () => {
        setStep('input');
        setSymptoms('');
        setQuestions([]);
        setAnswers({});
        setResult(null);
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6">
            {/* Header Info Banner */}
            <div className="bg-gradient-to-r from-teal-700 to-emerald-600 text-white p-6 rounded-2xl shadow-md flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                    <h2 className="text-xl font-bold flex items-center gap-2">
                        <Sparkles className="w-5 h-5 text-teal-200 animate-pulse" />
                        AI Clinical Triage Assistant
                    </h2>
                    <p className="text-xs text-teal-100 max-w-xl">
                        Powered by clinical decision-support models. Get immediate guidance on risk level, recommended specialist, precautions, and download official clinical reports.
                    </p>
                </div>
            </div>

            {/* Stepper Indicator */}
            <div className="flex items-center justify-center gap-2 text-xs font-semibold text-slate-400 select-none bg-white p-3 rounded-xl border border-slate-200 shadow-sm">
                <div className={`flex items-center gap-1.5 ${step === 'input' ? 'text-teal-600' : 'text-slate-500'}`}>
                    <span className={`w-5 h-5 rounded-full flex items-center justify-center border text-[10px] ${step === 'input' ? 'border-teal-600 bg-teal-50 text-teal-600' : 'border-slate-300'}`}>1</span>
                    Describe Symptoms
                </div>
                <div className="w-8 h-px bg-slate-200" />
                <div className={`flex items-center gap-1.5 ${step === 'questions' ? 'text-teal-600' : 'text-slate-500'}`}>
                    <span className={`w-5 h-5 rounded-full flex items-center justify-center border text-[10px] ${step === 'questions' ? 'border-teal-600 bg-teal-50 text-teal-600' : 'border-slate-300'}`}>2</span>
                    Clinical Clarification
                </div>
                <div className="w-8 h-px bg-slate-200" />
                <div className={`flex items-center gap-1.5 ${step === 'result' ? 'text-teal-600' : 'text-slate-500'}`}>
                    <span className={`w-5 h-5 rounded-full flex items-center justify-center border text-[10px] ${step === 'result' ? 'border-teal-600 bg-teal-50 text-teal-600' : 'border-slate-300'}`}>3</span>
                    Diagnostic Report
                </div>
            </div>

            {/* STEP 1: Symptoms & Language Input */}
            {step === 'input' && (
                <>
                    {/* Welcome & Featured Health Topic Hero Banner */}
                    <WelcomeHero
                        onExploreTriage={() => window.scrollTo({ top: 400, behavior: 'smooth' })}
                    />

                    <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-5">
                        <div>
                            <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2">
                                <Stethoscope className="w-5 h-5 text-teal-600" />
                                What symptoms are you experiencing?
                            </h3>
                            <p className="text-xs text-slate-500 mt-1">
                                Provide as much detail as possible, such as duration, severity, and any triggering factors.
                            </p>
                        </div>

                        <form onSubmit={handleStartTriage} className="space-y-4">
                            <div className="space-y-1.5">
                                <div className="flex items-center justify-between">
                                    <label className="block text-xs font-bold text-slate-700">
                                        Detailed Symptom Description
                                    </label>

                                    {/* Real-Time Audio Visualizer Voice-to-Text Button */}
                                    <button
                                        type="button"
                                        onClick={toggleVoiceInput}
                                        className={`flex items-center gap-2 px-3.5 py-1.5 rounded-xl text-xs font-semibold border transition-all duration-300 cursor-pointer ${isListening
                                                ? 'bg-rose-50 border-rose-300 text-rose-700 shadow-md ring-2 ring-rose-200'
                                                : 'bg-teal-50 text-teal-700 border-teal-200 hover:bg-teal-100 hover:border-teal-300 shadow-xs'
                                            }`}
                                    >
                                        {isListening ? (
                                            <>
                                                {/* Equalizer Soundwave Bars */}
                                                <div className="flex items-center gap-1 h-5 px-1">
                                                    <span className="wave-bar" style={{ height: `${Math.max(6, audioVolume * 0.25)}px` }} />
                                                    <span className="wave-bar" style={{ height: `${Math.max(8, audioVolume * 0.45)}px` }} />
                                                    <span className="wave-bar" style={{ height: `${Math.max(4, audioVolume * 0.35)}px` }} />
                                                    <span className="wave-bar" style={{ height: `${Math.max(10, audioVolume * 0.6)}px` }} />
                                                    <span className="wave-bar" style={{ height: `${Math.max(5, audioVolume * 0.3)}px` }} />
                                                </div>
                                                <span className="font-bold text-rose-600">Listening...</span>
                                                <span className="p-1 rounded-md bg-rose-200 text-rose-800 ml-1">
                                                    <Square className="w-2.5 h-2.5 fill-current" />
                                                </span>
                                            </>
                                        ) : (
                                            <>
                                                <Mic className="w-4 h-4 text-teal-600 animate-bounce" />
                                                <span>Speak Symptoms (Voice Input)</span>
                                            </>
                                        )}
                                    </button>
                                </div>

                                <textarea
                                    rows={5}
                                    placeholder="e.g., I have had a dull ache in my lower back for 3 days. It worsens when sitting down and is accompanied by mild stiffness in the mornings..."
                                    value={symptoms}
                                    onChange={(e) => setSymptoms(e.target.value)}
                                    className="w-full p-3.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none placeholder:text-slate-400 leading-relaxed"
                                />
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <div className="space-y-1.5">
                                    <label className="block text-xs font-bold text-slate-700 flex items-center gap-1.5">
                                        <Globe className="w-3.5 h-3.5 text-slate-400" />
                                        Preferred Report Language
                                    </label>
                                    <select
                                        value={i18n.language}
                                        onChange={(e) => {
                                            const selected = languages.find(l => l.code === e.target.value);
                                            if (selected) {
                                                handleLanguageSelect(selected.code, selected.langLabel);
                                            }
                                        }}
                                        className="w-full p-2.5 border border-slate-200 bg-white rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none cursor-pointer"
                                    >
                                        {languages.map((lang) => (
                                            <option key={lang.code} value={lang.code}>
                                                {lang.name}
                                            </option>
                                        ))}
                                    </select>
                                </div>
                            </div>

                            <div className="bg-amber-50/70 border border-amber-200/80 p-4 rounded-xl text-xs text-amber-900 leading-relaxed space-y-2">
                                <span className="font-bold block">💡 Tips for a better diagnostic prediction:</span>
                                <ul className="list-disc pl-4 space-y-1 text-amber-800">
                                    <li>Specify **when** the symptoms started (e.g. last night, 2 weeks ago).</li>
                                    <li>Mention what makes them **better or worse** (e.g. hot shower, walking, eating).</li>
                                    <li>Describe the **nature** of pain (e.g. sharp, dull ache, throbbing, burning).</li>
                                </ul>
                            </div>

                            <div className="flex justify-end">
                                <Button
                                    type="submit"
                                    isLoading={loading}
                                    className="px-6 py-3 bg-teal-600 hover:bg-teal-700 text-white font-semibold rounded-xl cursor-pointer"
                                    rightIcon={<ArrowRight className="w-4 h-4" />}
                                >
                                    Start Clinical Triage
                                </Button>
                            </div>
                        </form>
                    </div>

                    {/* Animated Testimonials Section */}
                    <TestimonialsSection />
                </>
            )}

            {/* STEP 2: Follow-up Questions */}
            {step === 'questions' && (
                <div className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-6">
                    <div>
                        <h3 className="text-lg font-bold text-slate-800 flex items-center gap-2">
                            <HelpCircle className="w-5 h-5 text-teal-600" />
                            AI Clarifying Questions
                        </h3>
                        <p className="text-xs text-slate-500 mt-1">
                            Please answer these questions to refine clinical precision and rule out urgent conditions.
                        </p>
                    </div>

                    <div className="space-y-6">
                        {questions.map((q, idx) => (
                            <div key={q.id} className="p-4 rounded-xl border border-slate-100 bg-slate-50/50 space-y-3">
                                <label className="block text-sm font-semibold text-slate-800">
                                    <span className="text-teal-600 mr-1.5 font-bold">Q{idx + 1}.</span>
                                    {q.question}
                                </label>

                                {q.options && q.options.length > 0 ? (
                                    <div className="flex flex-wrap gap-2.5">
                                        {q.options.map((option) => {
                                            const isSelected = answers[q.id] === option;
                                            return (
                                                <button
                                                    key={option}
                                                    type="button"
                                                    onClick={() => handleAnswerChange(q.id, option)}
                                                    className={`px-4 py-2 rounded-xl text-xs font-semibold border transition cursor-pointer ${isSelected
                                                        ? 'bg-teal-600 border-teal-600 text-white shadow-sm'
                                                        : 'bg-white border-slate-200 text-slate-600 hover:border-slate-300 hover:bg-slate-50'
                                                        }`}
                                                >
                                                    {option}
                                                </button>
                                            );
                                        })}
                                    </div>
                                ) : (
                                    <input
                                        type="text"
                                        placeholder="Type your response here..."
                                        value={answers[q.id] || ''}
                                        onChange={(e) => handleAnswerChange(q.id, e.target.value)}
                                        className="w-full p-2.5 border border-slate-200 bg-white rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                    />
                                )}
                            </div>
                        ))}
                    </div>

                    <div className="flex items-center justify-between border-t border-slate-100 pt-4">
                        <Button
                            variant="outline"
                            onClick={() => setStep('input')}
                            leftIcon={<ArrowLeft className="w-4 h-4" />}
                            disabled={loading}
                        >
                            Back
                        </Button>
                        <Button
                            onClick={() => handlePredictDiagnosis(false)}
                            isLoading={loading}
                            rightIcon={<Sparkles className="w-4 h-4" />}
                        >
                            Generate Assessment
                        </Button>
                    </div>
                </div>
            )}

            {/* STEP 3: Report & Interpretation */}
            {step === 'result' && result && (
                <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 animate-fade-in">

                    {/* Left Action Panel */}
                    <div className="lg:col-span-4 bg-white p-6 rounded-2xl border border-slate-200/80 shadow-xs h-fit space-y-4">
                        <div className="text-center pb-4 border-b border-slate-100">
                            <div className="w-14 h-14 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center mx-auto mb-3 border border-emerald-100 shadow-xs">
                                <CheckCircle className="w-7 h-7" />
                            </div>
                            <h4 className="font-bold text-slate-900 text-base">Assessment Complete</h4>
                            <p className="text-xs text-slate-400 mt-0.5">VAIDDISHA Clinical Report</p>
                        </div>

                        {result.pdf_download_path && (
                            <a
                                href={`${API_BASE_URL}/triage/download?file_path=${encodeURIComponent(result.pdf_download_path)}`}
                                target="_blank"
                                rel="noreferrer"
                                className="w-full inline-flex items-center justify-center gap-2 px-4 py-3 bg-teal-600 hover:bg-teal-700 text-white rounded-xl font-semibold text-xs transition-all shadow-xs hover:shadow-md hover:shadow-teal-600/20 active:scale-[0.98]"
                            >
                                <Download className="w-4 h-4" />
                                Download Official PDF Report
                            </a>
                        )}

                        <Button
                            variant="outline"
                            onClick={handleReset}
                            className="w-full text-xs py-2.5"
                            leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
                        >
                            Start New Checkup
                        </Button>

                        <div className="bg-amber-50/80 border border-amber-200/80 p-4 rounded-xl text-xs text-amber-900 leading-relaxed space-y-1.5">
                            <span className="font-bold flex items-center gap-1.5 text-amber-800">
                                <AlertCircle className="w-4 h-4 shrink-0" />
                                Clinical Disclaimer
                            </span>
                            <p className="text-[11px] text-amber-800/90 leading-normal">
                                AI triage assessments are clinical decision-support aids for informational purposes. They do not replace professional medical evaluations.
                            </p>
                        </div>
                    </div>

                    {/* Right Formatted Clinical Assessment Card */}
                    <div className="lg:col-span-8 bg-white p-6 sm:p-8 rounded-2xl border border-slate-200/80 shadow-xs flex flex-col min-h-[500px]">
                        <div className="flex items-center justify-between border-b border-slate-100 pb-4 mb-6">
                            <div className="flex items-center gap-2.5">
                                <div className="w-9 h-9 rounded-xl bg-teal-50 text-teal-600 border border-teal-100 flex items-center justify-center">
                                    <FileText className="w-5 h-5" />
                                </div>
                                <div>
                                    <h3 className="text-base font-bold text-slate-900">AI Clinical Diagnostic Summary</h3>
                                    <p className="text-[11px] text-slate-400">Structured differential assessment & recommendations</p>
                                </div>
                            </div>
                        </div>

                        {/* Markdown Viewer */}
                        <div className="flex-1 text-slate-700 leading-relaxed text-xs space-y-4">
                            <ReactMarkdown
                                components={{
                                    h1: ({ children }) => <h1 className="text-xl font-bold text-slate-900 border-b pb-2 mb-3">{children}</h1>,
                                    h2: ({ children }) => <h2 className="text-lg font-bold text-slate-900 mt-5 mb-2">{children}</h2>,
                                    h3: ({ children }) => <h3 className="text-sm font-bold text-slate-900 mt-4 mb-1.5 flex items-center gap-1.5">{children}</h3>,
                                    h4: ({ children }) => <h4 className="text-xs font-bold text-slate-800 mt-3 mb-1">{children}</h4>,
                                    p: ({ children }) => <p className="mb-3 text-slate-600 leading-relaxed">{children}</p>,
                                    strong: ({ children }) => <strong className="font-bold text-slate-900">{children}</strong>,
                                    ul: ({ children }) => <ul className="list-disc pl-5 space-y-1 my-2 text-slate-600">{children}</ul>,
                                    ol: ({ children }) => <ol className="list-decimal pl-5 space-y-1 my-2 text-slate-600">{children}</ol>,
                                    li: ({ children }) => <li className="leading-relaxed">{children}</li>,
                                    blockquote: ({ children }) => (
                                        <blockquote className="p-3.5 my-3 bg-rose-50 border-l-4 border-rose-500 rounded-r-xl text-rose-900 font-medium">
                                            {children}
                                        </blockquote>
                                    ),
                                    code: ({ children }) => (
                                        <code className="px-2 py-0.5 bg-teal-50 text-teal-700 rounded-md font-mono text-[11px] border border-teal-100">
                                            {children}
                                        </code>
                                    ),
                                    hr: () => <hr className="my-4 border-slate-100" />
                                }}
                            >
                                {result.analysis_markdown}
                            </ReactMarkdown>
                        </div>
                    </div>

                </div>
            )}
        </div>
    );
};

export default SymptomChecker;