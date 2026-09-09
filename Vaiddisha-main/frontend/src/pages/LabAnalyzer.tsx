// frontend/src/pages/LabAnalyzer.tsx
import React, { useState, useRef } from 'react';
import ReactMarkdown from 'react-markdown';
import { useToast } from '../context/ToastContext';
import { API_BASE_URL, labApi } from '../api';
import { Button } from '../components/common/Button';
import {
    UploadCloud,
    FileText,
    Activity,
    Scan,
    Download,
    AlertCircle,
    Trash2,
    Sparkles,
    CheckCircle2,
    ClipboardCheck,
    Stethoscope,
    ChevronDown,
    ChevronUp
} from 'lucide-react';

interface BiomarkerMetric {
    name: string;
    value: number | string;
    unit: string;
    referenceRange: string;
    status: 'normal' | 'borderline' | 'critical';
    progressPercent: number; // 0 to 100 for gauge visualization
}

export const LabAnalyzer: React.FC = () => {
    const { showToast } = useToast();

    const [selectedFile, setSelectedFile] = useState<File | null>(null);
    const [previewUrl, setPreviewUrl] = useState<string | null>(null);
    const [isScanning, setIsScanning] = useState(false);
    const [showFullReview, setShowFullReview] = useState(false);
    const [analysisResult, setAnalysisResult] = useState<{
        markdown: string;
        pdfPath?: string;
        metrics?: BiomarkerMetric[];
    } | null>(null);

    const fileInputRef = useRef<HTMLInputElement>(null);

    // File Drop / Selection Handlers
    const handleFileChange = (file: File) => {
        if (!file.type.startsWith('image/') && file.type !== 'application/pdf') {
            showToast('Please upload a valid lab report image (PNG, JPG, JPEG, WEBP) or PDF.', 'error');
            return;
        }

        if (file.size > 10 * 1024 * 1024) {
            showToast('File size exceeds the 10MB limit.', 'error');
            return;
        }

        setSelectedFile(file);
        if (file.type.startsWith('image/')) {
            const url = URL.createObjectURL(file);
            setPreviewUrl(url);
        } else {
            setPreviewUrl(null);
        }
    };

    const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFileChange(e.dataTransfer.files[0]);
        }
    };

    const handleClearFile = () => {
        setSelectedFile(null);
        if (previewUrl) {
            URL.revokeObjectURL(previewUrl);
            setPreviewUrl(null);
        }
        setAnalysisResult(null);
        if (fileInputRef.current) {
            fileInputRef.current.value = '';
        }
    };

    // Trigger OCR & LLM Analysis
    const handleAnalyzeReport = async () => {
        if (!selectedFile) {
            showToast('Please select or drop a medical lab report first.', 'error');
            return;
        }

        setIsScanning(true);
        try {
            const res = await labApi.analyzeReport(selectedFile);

            if (res.status === 'success') {
                setAnalysisResult({
                    markdown: res.analysis_markdown || res.text || 'Clinical analysis complete.',
                    pdfPath: res.pdf_download_path,
                    metrics: Array.isArray(res.metrics) ? res.metrics : undefined
                });
                setShowFullReview(false);
                showToast('Lab report analyzed successfully!', 'success');
            } else {
                throw new Error(res.message || 'Failed to extract data from the lab report.');
            }
        } catch (err: unknown) {
            const message = err instanceof Error ? err.message : 'OCR processing failed. Ensure the report image is clear.';
            showToast(message, 'error');
        } finally {
            setIsScanning(false);
        }
    };

    return (
        <div className="max-w-6xl mx-auto space-y-6 animate-fade-in">
            {/* Header Info Banner */}
            <div className="bg-gradient-to-r from-teal-700 to-emerald-600 text-white p-6 rounded-3xl shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div className="space-y-1">
                    <h2 className="text-xl font-bold flex items-center gap-2">
                        <Scan className="w-5 h-5 text-teal-200" />
                        Lab Vision OCR Analyzer
                    </h2>
                    <p className="text-xs text-teal-100 max-w-2xl leading-relaxed">
                        Upload diagnostic blood tests, metabolic panels, CBC reports, or biochemistry charts. Our multi-modal vision models extract biomarker data and highlight critical reference range deviations.
                    </p>
                </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
                {/* Left Column: Drag & Drop Upload Zone & Scan Preview */}
                <div className="lg:col-span-5 space-y-4">
                    <div className="bg-white rounded-3xl border border-slate-200/80 p-5 sm:p-6 shadow-xs space-y-4">
                        <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
                            <FileText className="w-4 h-4 text-teal-600" />
                            Upload Diagnostic Report
                        </h3>

                        {/* Dropzone Container */}
                        <div
                            onDragOver={(e) => e.preventDefault()}
                            onDrop={handleDrop}
                            onClick={() => !selectedFile && fileInputRef.current?.click()}
                            className={`relative border-2 border-dashed rounded-2xl p-6 text-center transition-all duration-200 flex flex-col items-center justify-center min-h-[220px] ${selectedFile
                                ? 'border-teal-400 bg-teal-50/20'
                                : 'border-slate-300 hover:border-teal-500 bg-slate-50/60 hover:bg-slate-50 cursor-pointer'
                                }`}
                        >
                            <input
                                ref={fileInputRef}
                                type="file"
                                accept="image/png,image/jpeg,image/webp,application/pdf"
                                className="hidden"
                                onChange={(e) => e.target.files?.[0] && handleFileChange(e.target.files[0])}
                            />

                            {previewUrl ? (
                                /* Image Preview with Laser Scanning Overlay */
                                <div className="relative w-full overflow-hidden rounded-xl group max-h-72">
                                    <img
                                        src={previewUrl}
                                        alt="Lab Report Preview"
                                        className="w-full h-auto object-contain rounded-xl max-h-64 mx-auto"
                                    />
                                    {isScanning && <div className="animate-scan-laser" />}

                                    <div className="absolute top-2 right-2 flex gap-1.5">
                                        <button
                                            type="button"
                                            onClick={(e) => {
                                                e.stopPropagation();
                                                handleClearFile();
                                            }}
                                            className="p-1.5 bg-rose-600/90 hover:bg-rose-700 text-white rounded-lg shadow-md transition cursor-pointer"
                                        >
                                            <Trash2 className="w-3.5 h-3.5" />
                                        </button>
                                    </div>
                                </div>
                            ) : selectedFile ? (
                                /* PDF / Document File Preview */
                                <div className="space-y-3 py-4 text-center">
                                    <div className="w-12 h-12 rounded-2xl bg-teal-100 text-teal-700 flex items-center justify-center mx-auto shadow-xs">
                                        <FileText className="w-6 h-6" />
                                    </div>
                                    <div>
                                        <p className="text-xs font-bold text-slate-800 truncate max-w-xs">{selectedFile.name}</p>
                                        <p className="text-[11px] text-slate-400">{(selectedFile.size / (1024 * 1024)).toFixed(2)} MB</p>
                                    </div>
                                    <Button
                                        variant="danger"
                                        size="sm"
                                        onClick={(e) => {
                                            e.stopPropagation();
                                            handleClearFile();
                                        }}
                                        leftIcon={<Trash2 className="w-3 h-3" />}
                                    >
                                        Remove File
                                    </Button>
                                </div>
                            ) : (
                                /* Empty Upload Prompt */
                                <div className="space-y-3 text-center">
                                    <div className="w-12 h-12 rounded-2xl bg-teal-50 text-teal-600 flex items-center justify-center mx-auto border border-teal-100 shadow-xs">
                                        <UploadCloud className="w-6 h-6" />
                                    </div>
                                    <div>
                                        <p className="text-xs font-bold text-slate-800">
                                            Click to upload <span className="text-teal-600 font-semibold">or drag and drop</span>
                                        </p>
                                        <p className="text-[11px] text-slate-400 mt-0.5">
                                            Supports JPG, PNG, JPEG, WEBP or PDF (first page scanned, Max 10MB)
                                        </p>
                                    </div>
                                </div>
                            )}
                        </div>

                        {/* Analyze Action Button */}
                        <Button
                            onClick={handleAnalyzeReport}
                            disabled={!selectedFile || isScanning}
                            isLoading={isScanning}
                            className="w-full py-3"
                            leftIcon={<Sparkles className="w-4 h-4 text-white" />}
                        >
                            {isScanning ? 'Executing OCR & Vision Analysis...' : 'Extract & Analyze Lab Report'}
                        </Button>
                    </div>

                    {/* Quick Help Card */}
                    <div className="bg-slate-100/70 border border-slate-200/80 p-4 rounded-2xl text-xs text-slate-600 space-y-1.5">
                        <span className="font-bold flex items-center gap-1.5 text-slate-800">
                            <AlertCircle className="w-3.5 h-3.5 text-teal-600" />
                            OCR Precision Advice
                        </span>
                        <p className="text-[11px] text-slate-500 leading-relaxed">
                            Ensure adequate lighting and that biomarker names and values (e.g., Fasting Sugar, Lipid Profile) are sharp and uncropped.
                        </p>
                    </div>
                </div>

                {/* Right Column: Visual Biomarker Range Meters & Structured Clinical Analysis */}
                <div className="lg:col-span-7 space-y-5">
                    {analysisResult ? (
                        <div className="space-y-5 animate-fade-in">
                            {/* Report Header */}
                            <div className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-950 via-slate-900 to-teal-950 p-6 sm:p-7 text-white shadow-lg shadow-slate-900/10">
                                <div className="absolute -right-10 -top-12 h-40 w-40 rounded-full border border-teal-300/20" />
                                <div className="absolute -right-2 -top-4 h-24 w-24 rounded-full border border-teal-300/15" />
                                <div className="relative flex flex-col sm:flex-row sm:items-end justify-between gap-5">
                                    <div className="space-y-3">
                                        <div className="inline-flex items-center gap-2 text-[10px] font-bold uppercase tracking-[0.18em] text-teal-300">
                                            <span className="h-1.5 w-1.5 rounded-full bg-emerald-400 shadow-[0_0_0_4px_rgba(52,211,153,0.15)]" />
                                            AI-assisted clinical review
                                        </div>
                                        <div>
                                            <h3 className="text-xl font-bold tracking-tight">Your report, made clearer</h3>
                                            <p className="mt-1.5 max-w-xl text-xs leading-relaxed text-slate-300">
                                                Biomarkers, reference ranges, and practical context brought together for a calmer review.
                                            </p>
                                        </div>
                                    </div>

                                    <div className="flex items-center gap-2">
                                        <span className="inline-flex items-center gap-1.5 rounded-full border border-emerald-300/20 bg-emerald-400/10 px-3 py-1.5 text-[10px] font-bold text-emerald-200">
                                            <CheckCircle2 className="h-3.5 w-3.5" /> Analysis complete
                                        </span>
                                        {analysisResult.pdfPath && (
                                            <a
                                                href={`${API_BASE_URL}/triage/download?file_path=${encodeURIComponent(analysisResult.pdfPath)}`}
                                                target="_blank"
                                                rel="noreferrer"
                                                className="inline-flex items-center gap-1.5 rounded-xl border border-white/15 bg-white/10 px-3 py-2 text-[11px] font-bold text-white transition hover:bg-white/20"
                                            >
                                                <Download className="h-3.5 w-3.5" /> Download
                                            </a>
                                        )}
                                    </div>
                                </div>
                            </div>

                            <div className="rounded-3xl border border-slate-200/80 bg-white p-6 sm:p-8 shadow-xs space-y-6">
                                <div className="flex items-center gap-3 border-b border-slate-100 pb-4">
                                    <div className="flex h-10 w-10 items-center justify-center rounded-2xl bg-teal-50 text-teal-700 ring-1 ring-teal-100">
                                        <Activity className="h-5 w-5" />
                                    </div>
                                    <div>
                                        <h3 className="text-base font-bold text-slate-900">Biomarker overview</h3>
                                        <p className="text-[11px] text-slate-400">Automated reference range classification</p>
                                    </div>
                                </div>

                            {/* Visual Biomarker Meters */}
                            {analysisResult.metrics && analysisResult.metrics.length > 0 && (
                                <div className="space-y-4">
                                    {analysisResult.metrics.map((metric, idx) => {
                                        const isNormal = metric.status === 'normal';
                                        const isBorderline = metric.status === 'borderline';

                                        return (
                                            <div key={idx} className="p-3.5 rounded-2xl bg-slate-50/80 border border-slate-200/60 space-y-2">
                                                <div className="flex items-center justify-between text-xs">
                                                    <span className="font-bold text-slate-800">{metric.name}</span>
                                                    <span
                                                        className={`px-2 py-0.5 rounded-md font-bold text-[10px] uppercase tracking-wider ${isNormal
                                                            ? 'bg-emerald-100 text-emerald-800'
                                                            : isBorderline
                                                                ? 'bg-amber-100 text-amber-800'
                                                                : 'bg-rose-100 text-rose-800'
                                                            }`}
                                                    >
                                                        {metric.status}
                                                    </span>
                                                </div>

                                                {/* Visual Progress Meter Bar */}
                                                <div className="space-y-1">
                                                    <div className="h-2 w-full bg-slate-200 rounded-full overflow-hidden">
                                                        <div
                                                            className={`h-full rounded-full transition-all duration-700 ${isNormal
                                                                ? 'bg-emerald-500'
                                                                : isBorderline
                                                                    ? 'bg-amber-500'
                                                                    : 'bg-rose-500'
                                                                }`}
                                                            style={{ width: `${Math.min(100, Math.max(10, metric.progressPercent))}%` }}
                                                        />
                                                    </div>

                                                    <div className="flex justify-between text-[11px] text-slate-500">
                                                        <span>
                                                            Observed: <strong className="text-slate-800 font-bold">{metric.value} {metric.unit}</strong>
                                                        </span>
                                                        <span>
                                                            Ref Range: <span className="font-medium text-slate-600">{metric.referenceRange}</span>
                                                        </span>
                                                    </div>
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            )}

                            {/* Formatted Markdown Clinical Summary */}
                            <div className="rounded-2xl border border-slate-200 bg-[#fffdfa] p-5 sm:p-6 shadow-[0_8px_30px_-24px_rgba(15,23,42,0.45)]">
                                <div className="mb-5 flex items-start gap-3 border-b border-slate-200/80 pb-4">
                                    <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-amber-50 text-amber-700 ring-1 ring-amber-100">
                                        <ClipboardCheck className="h-4 w-4" />
                                    </div>
                                    <div>
                                        <p className="text-[10px] font-bold uppercase tracking-[0.16em] text-amber-700">Clinical interpretation</p>
                                        <h4 className="mt-1 text-base font-bold text-slate-900">Quick clinical review</h4>
                                        <p className="mt-1 text-[11px] leading-relaxed text-slate-500">The key takeaways from your uploaded report, in plain language.</p>
                                    </div>
                                </div>

                                <div className={`relative overflow-hidden text-[13px] text-slate-700 leading-relaxed transition-[max-height] duration-300 ${showFullReview ? 'max-h-[2400px]' : 'max-h-[360px]'}`}>
                                    <ReactMarkdown
                                        components={{
                                            h1: ({ children }) => <h1 className="mt-6 border-b border-teal-100 pb-2 text-lg font-bold tracking-tight text-slate-950 first:mt-0">{children}</h1>,
                                            h2: ({ children }) => <h2 className="mt-7 flex items-center gap-2 border-b border-slate-200 pb-2 text-sm font-bold text-slate-950 before:h-4 before:w-1 before:rounded-full before:bg-teal-500">{children}</h2>,
                                            h3: ({ children }) => <h3 className="mt-5 mb-2 flex items-center gap-2 text-xs font-bold uppercase tracking-wide text-teal-800"><Stethoscope className="h-3.5 w-3.5" />{children}</h3>,
                                            p: ({ children }) => <p className="leading-7 text-slate-600">{children}</p>,
                                            strong: ({ children }) => <strong className="font-bold text-slate-950">{children}</strong>,
                                            ul: ({ children }) => <ul className="my-2 space-y-2 pl-5 text-slate-600 marker:text-teal-500">{children}</ul>,
                                            ol: ({ children }) => <ol className="my-2 list-decimal space-y-2 pl-5 text-slate-600 marker:font-bold marker:text-teal-700">{children}</ol>,
                                            li: ({ children }) => <li className="pl-1 leading-7">{children}</li>,
                                            hr: () => <hr className="my-6 border-slate-200" />,
                                            table: ({ children }) => <div className="my-4 overflow-x-auto rounded-xl border border-slate-200"><table className="w-full min-w-[520px] border-collapse text-xs">{children}</table></div>,
                                            thead: ({ children }) => <thead className="bg-slate-900 text-white">{children}</thead>,
                                            tbody: ({ children }) => <tbody className="divide-y divide-slate-100 bg-white">{children}</tbody>,
                                            tr: ({ children }) => <tr className="even:bg-slate-50">{children}</tr>,
                                            th: ({ children }) => <th className="whitespace-nowrap px-3 py-2.5 text-left text-[10px] font-bold uppercase tracking-wide">{children}</th>,
                                            td: ({ children }) => <td className="px-3 py-2.5 align-top text-slate-600">{children}</td>,
                                            blockquote: ({ children }) => (
                                                <blockquote className="my-4 rounded-r-xl border-l-4 border-amber-500 bg-amber-50 p-4 text-xs font-medium leading-6 text-amber-900">
                                                    {children}
                                                </blockquote>
                                            ),
                                            code: ({ children }) => (
                                                <code className="rounded-md border border-teal-100 bg-teal-50 px-1.5 py-0.5 font-mono text-[11px] text-teal-700">
                                                    {children}
                                                </code>
                                            )
                                        }}
                                    >
                                        {analysisResult.markdown}
                                    </ReactMarkdown>
                                    {!showFullReview && (
                                        <div className="pointer-events-none absolute inset-x-0 bottom-0 h-24 bg-gradient-to-t from-[#fffdfa] via-[#fffdfa]/90 to-transparent" />
                                    )}
                                </div>
                                <button
                                    type="button"
                                    onClick={() => setShowFullReview((visible) => !visible)}
                                    aria-expanded={showFullReview}
                                    className="inline-flex items-center gap-1.5 rounded-xl border border-teal-200 bg-teal-50 px-3 py-2 text-[11px] font-bold text-teal-800 transition hover:bg-teal-100"
                                >
                                    {showFullReview ? 'Show less' : 'Read full review'}
                                    {showFullReview ? <ChevronUp className="h-3.5 w-3.5" /> : <ChevronDown className="h-3.5 w-3.5" />}
                                </button>
                                <div className="mt-6 flex items-start gap-2.5 rounded-xl border border-slate-200 bg-slate-50/80 p-3.5 text-[10px] leading-relaxed text-slate-500">
                                    <Stethoscope className="mt-0.5 h-3.5 w-3.5 shrink-0 text-teal-600" />
                                    <span>This AI-generated interpretation is for educational support and does not replace advice from a qualified healthcare professional.</span>
                                </div>
                            </div>
                            </div>
                        </div>
                    ) : (
                        /* Placeholder State When No Report is Analyzed */
                        <div className="bg-white rounded-3xl border border-slate-200/80 p-12 text-center shadow-xs flex flex-col items-center justify-center min-h-[420px] space-y-3">
                            <div className="w-16 h-16 rounded-3xl bg-slate-50 text-slate-400 flex items-center justify-center border border-slate-100">
                                <Scan className="w-8 h-8" />
                            </div>
                            <div className="max-w-sm space-y-1">
                                <h4 className="text-sm font-bold text-slate-800">No Lab Report Analyzed Yet</h4>
                                <p className="text-xs text-slate-400 leading-relaxed">
                                    Upload a scanned lab test image or PDF on the left to review extracted biomarkers and clinical range classifications.
                                </p>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default LabAnalyzer;