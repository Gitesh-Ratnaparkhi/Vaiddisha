// frontend/src/pages/SymptomChecker.tsx
import { useState } from 'react';
import { triageApi, API_BASE_URL } from '../api';
import { useToast } from '../context/ToastContext';
import type { UserSession, TriageQuestion } from '../types';
import { Button } from '../components/common/Button';
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
  Globe
} from 'lucide-react';

interface SymptomCheckerProps {
    userSession: UserSession | null;
}

export default function SymptomChecker({ userSession }: SymptomCheckerProps) {
    const { showToast } = useToast();
    
    // Step state: 'input' | 'questions' | 'result'
    const [step, setStep] = useState<'input' | 'questions' | 'result'>('input');
    const [symptoms, setSymptoms] = useState('');
    const [targetLanguage, setTargetLanguage] = useState('English');
    const [questions, setQuestions] = useState<TriageQuestion[]>([]);
    const [answers, setAnswers] = useState<Record<string, string>>({});
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<{ analysis_markdown: string; pdf_download_path: string } | null>(null);

    // Languages supported by backend i18n
    const languages = [
        { code: 'English', name: 'English' },
        { code: 'Hindi', name: 'हिंदी (Hindi)' },
        { code: 'Marathi', name: 'मराठी (Marathi)' },
        { code: 'Spanish', name: 'Español (Spanish)' }
    ];

    // Stage 1: Get follow-up questions based on symptoms
    const handleStartTriage = async (e: React.FormEvent) => {
        e.preventDefault();
        if (!symptoms.trim()) {
            showToast('Please describe your symptoms to begin.', 'error');
            return;
        }

        setLoading(true);
        try {
            const res = await triageApi.getQuestions({ symptoms });
            if (res.questions && res.questions.length > 0) {
                setQuestions(res.questions);
                // Initialize empty answers for each question
                const initialAnswers: Record<string, string> = {};
                res.questions.forEach((q: TriageQuestion) => {
                    initialAnswers[q.id] = '';
                });
                setAnswers(initialAnswers);
                setStep('questions');
                showToast('Follow-up questions generated successfully.', 'success');
            } else {
                // If no questions are returned, proceed straight to prediction
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
            // Format triage answers as "Question: Answer | Question: Answer"
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
                patient_email: userSession?.email || undefined,
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
            {/* Header info banner */}
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
                {!userSession && (
                    <div className="bg-white/10 backdrop-blur border border-white/20 p-3 rounded-xl text-xs flex items-start gap-2.5 max-w-xs">
                        <AlertCircle className="w-4 h-4 text-amber-300 shrink-0 mt-0.5" />
                        <div>
                            <span className="font-semibold block text-amber-200">Guest Mode</span>
                            Your consultation will not be saved. Sign In to persist your records.
                        </div>
                    </div>
                )}
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
                            <label className="block text-xs font-bold text-slate-700">Detailed Symptom Description</label>
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
                                    value={targetLanguage}
                                    onChange={(e) => setTargetLanguage(e.target.value)}
                                    className="w-full p-2.5 border border-slate-200 bg-white rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                                >
                                    {languages.map((lang) => (
                                        <option key={lang.code} value={lang.code}>
                                            {lang.name}
                                        </option>
                                    ))}
                                </select>
                            </div>
                        </div>

                        <div className="bg-slate-50 border border-slate-200/80 p-4 rounded-xl text-xs text-slate-600 leading-relaxed space-y-2">
                            <span className="font-bold text-slate-700 block">💡 Tips for a better diagnostic prediction:</span>
                            <ul className="list-disc pl-4 space-y-1">
                                <li>Specify **when** the symptoms started (e.g. last night, 2 weeks ago).</li>
                                <li>Mention what makes them **better or worse** (e.g. hot shower, walking, eating).</li>
                                <li>Describe the **nature** of pain (e.g. sharp, dull ache, throbbing, burning).</li>
                            </ul>
                        </div>

                        <div className="flex justify-end">
                            <Button
                                type="submit"
                                isLoading={loading}
                                className="px-6 py-3"
                                rightIcon={<ArrowRight className="w-4 h-4" />}
                            >
                                Start Clinical Triage
                            </Button>
                        </div>
                    </form>
                </div>
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
                            Please answer these questions from Vaiddisha AI to refine clinical precision and rule out urgent conditions.
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
                                                    className={`px-4 py-2 rounded-xl text-xs font-semibold border transition ${
                                                        isSelected
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
                            Back to Symptoms
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
                    {/* Left Actions Card */}
                    <div className="lg:col-span-4 bg-white p-5 rounded-2xl border border-slate-200 shadow-sm h-fit space-y-4">
                        <div className="text-center pb-4 border-b border-slate-100">
                            <div className="w-12 h-12 bg-emerald-50 text-emerald-600 rounded-full flex items-center justify-center mx-auto mb-3 border border-emerald-100">
                                <CheckCircle className="w-6 h-6" />
                            </div>
                            <h4 className="font-bold text-slate-800 text-sm">Assessment Complete</h4>
                            <p className="text-[11px] text-slate-400 mt-0.5">VAIDDISHA Medical Report generated</p>
                        </div>

                        {result.pdf_download_path && (
                            <a
                                href={`${API_BASE_URL}/triage/download?file_path=${encodeURIComponent(result.pdf_download_path)}`}
                                target="_blank"
                                rel="noreferrer"
                                className="w-full inline-flex items-center justify-center gap-2 px-4 py-2.5 bg-teal-600 hover:bg-teal-700 text-white rounded-xl font-semibold text-xs transition shadow-sm"
                            >
                                <Download className="w-4 h-4" />
                                Download PDF Report
                            </a>
                        )}

                        <Button
                            variant="outline"
                            onClick={handleReset}
                            className="w-full text-xs"
                            leftIcon={<RefreshCw className="w-3.5 h-3.5" />}
                        >
                            Start New Checkup
                        </Button>

                        <div className="bg-amber-50 border border-amber-200/60 p-3.5 rounded-xl text-[11px] text-amber-800 leading-relaxed space-y-1">
                            <span className="font-bold block flex items-center gap-1">
                                <AlertCircle className="w-3.5 h-3.5 shrink-0" />
                                Clinical Disclaimer:
                            </span>
                            AI triage assessments are informational tools and do not substitute professional medical care, diagnosis, or treatment. If experiencing an emergency, please visit the nearest emergency room immediately.
                        </div>
                    </div>

                    {/* Diagnostic Findings Column */}
                    <div className="lg:col-span-8 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col min-h-[400px]">
                        <h3 className="text-lg font-bold text-slate-800 mb-3 border-b border-slate-100 pb-3 flex items-center gap-2">
                            <FileText className="w-5 h-5 text-teal-600" />
                            AI Clinical Interpretation & Recommendations
                        </h3>

                        <div className="flex-1 prose prose-sm max-w-none text-slate-700 whitespace-pre-wrap leading-relaxed">
                            {result.analysis_markdown}
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
}
