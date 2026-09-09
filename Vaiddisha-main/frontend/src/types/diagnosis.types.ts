// frontend/src/types/diagnosis.types.ts

export type UrgencyLevel = 'Low' | 'Moderate' | 'High' | 'Emergency';

export interface TriageQuestion {
    id: string;
    question: string;
    options?: string[];
}

export interface ConditionPrediction {
    disease_name: string;
    confidence_score: number;
    description: string;
    precautions: string[];
}

export interface DiagnosticAssessmentResponse {
    patient_email?: string;
    summary: string;
    urgency_level: UrgencyLevel;
    recommended_specialty: string;
    likely_conditions: ConditionPrediction[];
    safety_warnings: string[];
    analysis_markdown: string;
    pdf_download_path?: string;
}