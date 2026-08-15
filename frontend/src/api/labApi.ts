// frontend/src/api/labApi.ts
import { apiClient } from './client';

export const labApi = {
    analyzeReport: async (file: File, notes: string = '', language: string = 'English') => {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('notes', notes);
        formData.append('language', language);

        const res = await apiClient.post('/lab/analyze', formData, {
            headers: {
                'Content-Type': 'multipart/form-data',
            },
        });
        return res.data;
    },
};