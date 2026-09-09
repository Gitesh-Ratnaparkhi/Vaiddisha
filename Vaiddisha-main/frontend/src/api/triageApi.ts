// frontend/src/api/triageApi.ts
import { apiClient } from './client';

export interface TriageQuestionsPayload {
    symptoms: string;
}

export interface PredictDiagnosisPayload {
    symptoms: string;
    triage_answers?: string;
    patient_email?: string;
    target_language?: string;
}

export const triageApi = {
    getQuestions: async (payload: TriageQuestionsPayload) => {
        const res = await apiClient.post('/triage/questions', payload);
        return res.data;
    },
    predictDiagnosis: async (payload: PredictDiagnosisPayload) => {
        const res = await apiClient.post('/triage/predict', payload);
        return res.data;
    },
};