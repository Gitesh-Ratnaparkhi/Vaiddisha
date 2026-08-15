// frontend/src/pages/LabAnalyzer.tsx
import { useState, type FormEvent } from 'react';
import { labApi } from '../api';
import { useToast } from '../context/ToastContext';
import { UploadCloud, FileText } from 'lucide-react';
import { Button } from '../components/common/Button';

export default function LabAnalyzer() {
    const { showToast } = useToast();
    const [file, setFile] = useState<File | null>(null);
    const [notes, setNotes] = useState('');
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState<string | null>(null);

    const handleUpload = async (e: FormEvent) => {
        e.preventDefault();
        if (!file) {
            showToast('Please select a lab report image (PNG/JPG).', 'error');
            return;
        }

        setLoading(true);
        try {
            const res = await labApi.analyzeReport(file, notes, 'English');
            setResult(res.findings_markdown || res.summary || JSON.stringify(res, null, 2));
            showToast('Lab report analyzed successfully!', 'success');
        } catch (err: any) {
            showToast(err.message || 'Failed to analyze lab document.', 'error');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Upload Column */}
            <div className="lg:col-span-5 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm space-y-4">
                <div>
                    <h2 className="text-lg font-bold text-slate-800">Lab Report Vision OCR</h2>
                    <p className="text-xs text-slate-500">
                        Upload blood work, lipid panels, or pathology images for automated extraction.
                    </p>
                </div>

                <form onSubmit={handleUpload} className="space-y-4">
                    <div className="border-2 border-dashed border-slate-200 rounded-2xl p-6 text-center hover:border-teal-500 transition cursor-pointer">
                        <input
                            type="file"
                            accept="image/png, image/jpeg, image/jpg"
                            onChange={(e) => setFile(e.target.files?.[0] || null)}
                            className="hidden"
                            id="lab-upload"
                        />
                        <label htmlFor="lab-upload" className="cursor-pointer flex flex-col items-center">
                            <UploadCloud className="w-10 h-10 text-teal-600 mb-2" />
                            <span className="text-sm font-semibold text-slate-700">
                                {file ? file.name : 'Click or drag lab report image here'}
                            </span>
                            <span className="text-[11px] text-slate-400 mt-1">Supports PNG, JPG (Max 10MB)</span>
                        </label>
                    </div>

                    <div className="space-y-1.5">
                        <label className="block text-xs font-semibold text-slate-700">Additional Clinical Context (Optional)</label>
                        <input
                            type="text"
                            placeholder="e.g. Fasting 12 hours, routine annual checkup..."
                            value={notes}
                            onChange={(e) => setNotes(e.target.value)}
                            className="w-full p-2.5 border border-slate-200 rounded-xl text-sm focus:ring-2 focus:ring-teal-500 focus:outline-none"
                        />
                    </div>

                    <Button
                        type="submit"
                        isLoading={loading}
                        className="w-full py-3"
                        leftIcon={<FileText className="w-4 h-4" />}
                    >
                        Extract & Analyze Values
                    </Button>
                </form>
            </div>

            {/* Result Column */}
            <div className="lg:col-span-7 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm min-h-[400px]">
                <h2 className="text-lg font-bold text-slate-800 mb-3 border-b border-slate-100 pb-3">
                    Lab Findings & Clinical Interpretation
                </h2>

                {result ? (
                    <div className="prose prose-sm max-w-none text-slate-700 whitespace-pre-wrap leading-relaxed">
                        {result}
                    </div>
                ) : (
                    <div className="h-64 flex flex-col items-center justify-center text-slate-400 text-sm">
                        <FileText className="w-12 h-12 mb-2 text-slate-300" />
                        Upload a lab report image to preview extracted markers and reference ranges.
                    </div>
                )}
            </div>
        </div>
    );
}