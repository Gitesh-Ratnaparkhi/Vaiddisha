// frontend/src/types/lab.types.ts

export interface LabAnalysisResponse {
    findings_markdown: string;
    abnormal_markers: Array<{
        test_name: string;
        value: string;
        reference_range: string;
        status: 'High' | 'Low' | 'Normal';
    }>;
    summary: string;
    recommended_action: string;
}